import typing

from pydantic import BaseModel, Field

from .winwin import RootWithdraw, RootUserVideo, UserLevels


class UserMainAdminInfo(BaseModel):
    id: typing.Optional[int] = None
    name: typing.Optional[str] = None
    phone_number: typing.Optional[int] = None
    created_at: int = None
    levels: UserLevels = None


class DataVideoItem(BaseModel):
    user: UserMainAdminInfo
    data: RootUserVideo


class DataWithdrawItem(BaseModel):
    user: UserMainAdminInfo
    data: RootWithdraw


class PendingModerationVideoResponse(BaseModel):
    data: typing.List[DataVideoItem]


class PendingModerationWithdrawResponse(BaseModel):
    data: typing.List[DataWithdrawItem]


class VideosResponse(BaseModel):
    data: typing.List[DataVideoItem]


class TopEarningAccount(BaseModel):
    user_id: int = Field(..., description="ID пользователя")
    cpm: float = Field(..., description="Сумма заработка по CPM")
    pps: float = Field(..., description="Сумма заработка по PPS")
    ppc: float = Field(..., description="Сумма заработка по PPC")
    total_amount: float = Field(..., description="Общая сумма заработка")
    current_amount: float = Field(..., description="Текущая сумма заработка")


class TopEarningAccountsResponse(BaseModel):
    data: typing.List[TopEarningAccount]


class Video(BaseModel):
    id: typing.Optional[int] = None
    video_id: int
    title: typing.Optional[str] = None
    thumbnail: typing.Optional[str] = None
    duration: typing.Optional[float] = None
    video_url: typing.Optional[str] = None
    view_count: typing.Optional[int] = None
    like_count: typing.Optional[int] = None
    comment_count: typing.Optional[int] = None
    current_cpm_level: int = 1
    new_views: int = 0
    created_at: int
    transaction_id: typing.Optional[int] = None
    amount: typing.Optional[float] = 0


class VideoTable(BaseModel):
    data: typing.List[Video] = None


class PPCDataItem(BaseModel):
    all_users: int = 0
    active_users: int = 0


class PPCData(BaseModel):
    user: UserMainAdminInfo
    data: PPCDataItem


class PPCStat(BaseModel):
    data: typing.List[PPCData] = None


class PPSDataItem(BaseModel):
    id: int
    user_id: int
    purchase_id: int
    purchuase_sum: int
    current_pps_level: int = 1
    transaction_id: int
    transaction_sum: int
    created_at: int


class PPSData(BaseModel):
    user: UserMainAdminInfo
    data: PPSDataItem


class PPSStat(BaseModel):
    data: typing.List[PPSData] = None


class UserBanData(BaseModel):
    id: typing.Optional[int] = None
    user_id: typing.Optional[int] = None
    ban_reason: typing.Optional[str] = None
    created_at: typing.Optional[int] = None


class UserBan(BaseModel):
    data: UserBanData
