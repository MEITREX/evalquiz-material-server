import asyncio
from evalquiz_proto.shared.generated import MaterialServerBase, Empty, ListOfStrings, MaterialUploadData, String, LectureMaterial
from grpclib.server import Server
from typing import AsyncIterator
from evalquiz_proto.shared import InternalMaterialController


class MaterialServerService(MaterialServerBase):

    def __init__(self):
        self.internal_material_controller = InternalMaterialController()

    async def upload_material(
        self, material_upload_data_iterator: AsyncIterator["MaterialUploadData"]
    ) -> "Empty":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

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
