"""
Make some easy-to-use api from basic wrappers.
"""
from ..type import (FeedData, FeedDetailRep, FeedMoreAux, FeedRep, FeedsCount, FloatViewPhoto)
from .raw import QzoneApi


class DummyQapi(QzoneApi):
    async def feeds3_html_more(self, pagenum: int, trans: QzoneApi.FeedsMoreTransaction = None):
        r = await super().feeds3_html_more(pagenum, trans=trans)
        data = r['data']
        main = r['main']
        return [FeedRep.parse_obj(i) for i in data], FeedMoreAux.parse_obj(main)

    async def emotion_getcomments(self, feedData: FeedData):
        r = await super().emotion_getcomments(feedData)
        return str.strip(r['newFeedXML'])

    async def emotion_msgdetail(self, owner: int, fid: str):
        r = await super().emotion_msgdetail(owner, fid)
        return FeedDetailRep.parse_obj(r)

    async def get_feeds_count(self):
        r = await super().get_feeds_count()
        return FeedsCount.parse_obj(r)

    async def floatview_photo_list(self, album: QzoneApi.AlbumData, num: int):
        r = await super().floatview_photo_list(album, num)
        return [FloatViewPhoto.parse_obj(i) for i in r['photos']]
