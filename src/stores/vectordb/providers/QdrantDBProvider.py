from ..VectorDBInterface import VectorDBInterface
import logging
from ..VectorDBEnums import DistanceMethodEnums
from qdrant_client import models,QdrantClient
from typing import List
from models.db_shemes import RetrievedDocument


class QdrantDBProvider(VectorDBInterface):

    def __init__(self,db_path,distance_method:str):

        # each database has client 
        # i will define it's value inside connect method
        self.client = None
        self.db_path = db_path
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):
        # ensure first that this collection i want to delete is existed
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)

    def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        
        if do_reset:
            _ = self.delete_collection(collection_name=collection_name)
        
        if not self.is_collection_existed(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )

            return True
        
        return False

        
    def insert_one(
        self,
        collection_name: str,
        text: str,
        vector: list,
        metadata: dict = None,
        record_id: str = None,
    ):
        if not self.is_collection_existed(collection_name):
            self.logger.error(
                f"Collection does not exist: {collection_name}"
            )
            return False

        try:
            point_id = record_id if record_id is not None else 0

            self.client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "text": text,
                            "metadata": metadata,
                        },
                    )
                ],
                wait=True,
            )
            return True

        except Exception as e:
            self.logger.exception(f"Error inserting record: {e}")
            return False


    def insert_many(
        self,
        collection_name: str,
        texts: list,
        vectors: list,
        metadata: list = None,
        record_ids: list = None,
        batch_size: int = 50,
    ):
        if not self.is_collection_existed(collection_name):
            self.logger.error(
                f"Collection does not exist: {collection_name}"
            )
            return False

        if len(texts) != len(vectors):
            self.logger.error("Texts and vectors lengths do not match")
            return False

        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(len(texts)))

        if not (
            len(texts) == len(metadata) == len(record_ids)
        ):
            self.logger.error("Texts, metadata, and IDs lengths do not match")
            return False

        try:
            for i in range(0, len(texts), batch_size):
                end = min(i + batch_size, len(texts))

                batch_records = [
                    models.PointStruct(
                        id=record_ids[j],
                        vector=vectors[j],
                        payload={
                            "text": texts[j],
                            "metadata": metadata[j],
                        },
                    )
                    for j in range(i, end)
                ]

                self.client.upsert(
                    collection_name=collection_name,
                    points=batch_records,
                    wait=True,
                )

            return True

        except Exception as e:
            self.logger.exception(f"Error while inserting batch: {e}")
            return False


    

    def debug_collection(self, collection_name: str):
        info = self.client.get_collection(
            collection_name=collection_name
        )

        print("Collection:", collection_name)
        print("Points count:", info.points_count)
        print("Vector config:", info.config.params.vectors)

    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):

        results= self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit,
            
        ).points
        if not results :
            return None

        return [
            RetrievedDocument(**{
                "score":result.score,
                "text":result.payload["text"]

            })
            for result in results
        ]

        
    
    

        