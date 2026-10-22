from .BaseDataModel import BaseDataModel
from .db_shemes.asset import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import objectid

# BaseDataModel: Provides the database connection and collection setup.
# Project: Defines the structure and validation rules for a project.
# DataBaseEnum: Stores predefined collection names, such as "projects"



class AssetModel(BaseDataModel):

    def __init__(self, db_client:object):
            super().__init__(db_client)
            self.collection=self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
    
    async def init_collection(self):
        all_collections= await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection=self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes=Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(index["key"],
                                                name=index['name'],
                                                unique=index['unique'])
    
    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance
    
    async def create_Asset(self,asset:Asset):

        result=await self.collection.insert_one(asset.model_dump(by_alias=True,exclude_unset=True))
        asset.id=result.inserted_id

        return asset

    async def get_all_project_assets(self, asset_project_id: str):

        return await self.collection.find({
            "asset_project_id":objectid(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id
        
        }).to_list(length=None)

    

    
        