import typing
from typing import Optional

from pydantic import BaseModel, validator


class UserLevels(BaseModel):
    cpm: Optional[int] = 1
    pps: Optional[int] = 1
    ppc: Optional[int] = 1


class RootVideo(BaseModel):
    id: int = None
    video_id: Optional[str] = None
    video_type_id: int = None
    title: Optional[str] = None
    duration: Optional[float] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    current_cpm_level: Optional[int] = 1
    new_views: Optional[int] = 0
    created_at: Optional[int] = None
    thumbnail: Optional[str] = None
    video_url: Optional[str] = None

    @validator("video_url", always=True)
    def create_video_url_param(cls, v, values):
        video_id = values.get("video_id")
        video_type_id = values.get("video_type_id")
        if not video_id or video_type_id is None:
            return None

        video_types = {
            1: f"https://www.tiktok.com/t/{video_id}",
            2: f"https://www.instagram.com/reel/{video_id}/",
            3: f"https://www.youtube.com/watch?v={video_id}",
            4: f"https://www.youtube.com/shorts/{video_id}",
        }

        return video_types.get(video_type_id, None)


class UserVideo(RootVideo):
    updated_at: int = None
    moderated_at: int = None
    stopped_at: int = None
    is_accepted: int = None
    earned: float = None


class RootUserVideo(BaseModel):
    id: int = None
    user_id: int = None
    video_id: str = None
    created_at: int = None
    moderated_at: int = None
    is_accepted: int = None
    stopped_at: int = None
    video_type_id: int = None
    video_url: str = None

    @validator("video_url", always=True)
    def create_video_url_param(cls, v, values):
        video_id = values.get("video_id")
        video_type_id = values.get("video_type_id")
        if not video_id or video_type_id is None:
            return None

        video_types = {
            1: f"https://www.tiktok.com/t/{video_id}",
            2: f"https://www.instagram.com/reel/{video_id}/",
            3: f"https://www.youtube.com/watch?v={video_id}",
            4: f"https://www.youtube.com/shorts/{video_id}",
        }

        return video_types.get(video_type_id, None)


class RootUnsentRequests(BaseModel):
    user_id: int = None
    source_id: int = None
    request_type: str = None
    created_at: int = None


class AddUserVideo(BaseModel):
    user_id: int
    video_id: str
    unique_video_id: str = None
    video_type_id: int
    created_at: int


class Video(RootVideo):
    video_id: int = None
    transaction_id: Optional[int] = None


class UserStat(BaseModel):
    cpm: Optional[float] = 0
    pps: Optional[float] = 0
    ppc: Optional[float] = 0
    cpm_on_hold: Optional[float] = 0
    pps_on_hold: Optional[float] = 0
    ppc_on_hold: Optional[float] = 0
    canceled_withdraw: Optional[float] = 0
    total_balance: Optional[float] = 0
    monthly_views: Optional[int] = 0
    total_views: Optional[int] = 0
    total_sales: Optional[int] = 0
    monthly_sales: Optional[int] = 0
    monthly_clicks: Optional[int] = 0
    total_clicks: Optional[int] = 0
    total_active_clicks: Optional[int] = 0
    total_real_clicks: Optional[int] = 0
    cpm_monthly_earnings: Optional[float] = 0
    pps_monthly_earnings: Optional[float] = 0
    ppc_monthly_earnings: Optional[float] = 0


class UserRoot(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    phone_number: Optional[int] = None
    created_at: int = None


class UserWithdraw(BaseModel):
    id: Optional[int] = None
    sum: Optional[float] = None
    cryptocurrency_sum: Optional[float] = None
    method: Optional[str] = None
    cryptocurrency: Optional[str] = None
    wallet_address: Optional[str] = None
    created_at: Optional[int] = None
    moderated_at: Optional[int] = None
    is_accepted: Optional[int] = 0


class RootWithdraw(UserWithdraw):
    user_id: Optional[int] = None
    transaction_id: Optional[int] = None


class User(UserRoot):
    levels: UserLevels = None
    videos: typing.List[UserVideo] = None
    stat: UserStat = None
    referral_code: str = None
    withdrawals: typing.List[UserWithdraw] = None
    referral_link: str = None


class RootCPMReward(BaseModel):
    video_type_id: int = None
    reward: float = None


class RootCPMLevel(BaseModel):
    min_views: int = None
    duration: int = None
    rewards: typing.List[RootCPMReward] = None


class RootPPSReward(BaseModel):
    rate: float
    bonus_rate: typing.Optional[float] = None
    bonus_rate_min_price: typing.Optional[float] = None


class RootPPCReward(BaseModel):
    rate: float
    bonus_rate: typing.Optional[float] = None
    bonus_rate_min_activities: typing.Optional[int] = None


class RootPPSLevel(BaseModel):
    min_sales: int
    rewards: RootPPSReward = None


class RootPPCLevel(BaseModel):
    min_clicks: int
    rewards: RootPPCReward = None


class VideoType(BaseModel):
    id: int
    type_name: str


class Conf(BaseModel):
    cpm: typing.List[RootCPMLevel]
    pps: typing.List[RootPPSLevel]
    ppc: typing.List[RootPPCLevel]
    video_types: typing.List[VideoType]
    min_withdraw: int = 20
    withdraw_cryptocurrencies: typing.List = ["ton", "not"]


class Root(BaseModel):
    user: User
    conf: Conf


class UserPurchase(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    purchase_id: Optional[int] = None
    purchase_sum: Optional[float] = None
    current_pps_level: Optional[int] = None
    transaction_id: Optional[int] = None
    created_at: Optional[int] = None


class LeaderboardBoard(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    earnings: Optional[float] = 0
    views: Optional[int] = 0
    sales: Optional[int] = 0
    clicks: Optional[int] = 0
    registered_at: Optional[int] = None


class LeaderboardMe(LeaderboardBoard):
    position: Optional[int] = None
    max_position: Optional[int] = position


class LeaderboardRoot(BaseModel):
    me: LeaderboardMe = None
    board: typing.List[typing.List[LeaderboardBoard]] = None
