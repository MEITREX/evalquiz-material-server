import asyncio
from evalquiz_proto.shared.exceptions import (
    DataChunkNotBytesException,
    EmptyUploadException,
    FirstDataChunkNotLectureMaterialException,
)
from evalquiz_proto.shared.generated import (
    MaterialServerBase,
    Empty,
    ListOfStrings,
    MaterialUploadData,
    String,
    LectureMaterial,
)
from grpclib.server import Server
from typing import AsyncIterator, List, Union
from evalquiz_proto.shared import InternalMaterialController
import betterproto


class MaterialServerService(MaterialServerBase):
    """Serves endpoints for material manipulation."""

    def __init__(self):
        self.internal_material_controller = InternalMaterialController()

    async def upload_material(
        self, material_upload_data_iterator: AsyncIterator["MaterialUploadData"]
    ) -> "Empty":
        material_upload_data = [gen async for gen in material_upload_data_iterator()]
        self._validate_material_upload_data(material_upload_data)
        lecture_material = material_upload_data[0]
        for data in material_upload_data[1:]:
            with open("file.txt", "wb") as binary_file:
                binary_file.write(data)

    def _validate_material_upload_data(material_upload_data: List[Union[LectureMaterial, bytes]]) -> None:
        if len(material_upload_data) != 0:
            lecture_material = material_upload_data[0]
            type = betterproto.which_one_of(lecture_material, "material_upload_data")[0]
            if type != "lecture_material":
                FirstDataChunkNotLectureMaterialException()
            for data in material_upload_data[1:]:
                if type != "data":
                    raise DataChunkNotBytesException()
        else:
            raise EmptyUploadException()

    async def delete_material(self, string: "String") -> "Empty":
        self.internal_material_controller.delete_material(string)
        return Empty()

    async def get_material_hashes(self, empty: "Empty") -> "ListOfStrings":
        material_hashes = self.internal_material_controller.get_material_hashes
        return ListOfStrings(material_hashes)

    async def get_material(self, string: "String") -> "LectureMaterial":
        return self.internal_material_controller.get_material_from_hash(string)


async def main():
    server = Server([MaterialServerService()])
    await server.start("127.0.0.1", 50051)
    await server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
