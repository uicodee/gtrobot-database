from .base import Base, BaseModel

# 15 tables (done)
from .activated_user_sections import ActivatedUserSections
from .admin_settings import AdminSettings
from .course_placeholders import CoursePlaceholders
from .premium_users import PremiumUsers
from .profiles import Profile
from .referrals import Referrals
from .quiz_results import QuizResults
from .reply_messages import ReplyMessages
from .social_networks_links import SocialNetworksLinks
from .subscription_orders import SubscriptionOrders
from .subscription_services import SubscriptionServices
from .subscriptions import Subscriptions
from .user_services import UserServices
from .user_tokens import UserTokens
from .users import User
from .users_exchange import UsersExchange

# 5 tables (done)
from .closed_leaderboard_orders import ClosedLeaderboardOrders
from .leaderboard_orders import LeaderboardOrders
from .leaderboard_users import LeaderboardUsers
from .auto_order_users import AutoOrderUsers
from .auto_order_users_orders import AutoOrderUsersOrders

# 4 tables (done)
from .forex_signals import ForexSignals
from .forex_users import ForexUsers
from .users_forex_api import UsersForexAPI
from .forex_users_order_history import ForexUsersOrderHistory

# 2 tables (done)
from .klines_pairs import KlinesPairs
from .klines_users import KlinesUsers

# 17 tables (done)
from .balance_history import BalanceHistory
from .budget_history import BudgetHistory
from .holding_balances import HoldingBalances
from .mining_history import MiningHistory
from .mining_referrals import MiningReferrals
from .subscribers_mining import SubscribersMining
from .mining_subscription_orders import MiningSubscriptionOrders
from .mining_tasks import MiningTasks
from .user_earnings import UserEarnings
from .user_exchanges import UserExchanges
from .user_mining_history import UserMiningHistory
from .user_promo_codes import UserPromoCodes
from .user_subscriptions import UserSubscriptions
from .user_tasks import UserTasks
from .user_withdraws import UserWithdraws
from .mining_users import MiningUsers
from .withdraw_transactions import WithdrawTransactions

# 4 tables (done)
from .payment_numbers import PaymentNumbers
from .purchases import Purchases
from .uzum_app_payment import UzumAppPayment
from .uzum_payment import UzumPayment

# 4 tables (p2p) (done)
from .auto_delete_message import AutoDeleteMessage
from .p2p_pairs import P2PPairs
from .p2p_pairs_exchange import P2PPairsExchange
from .p2p_users import P2PUsers

# 3 tables (done)
from .pairs import Pairs
from .signals_users import SignalsUsers
from .xauusd_signals import XAUUSDSignals

# 3 tables (done)
from .affiliate_users import AffiliateUsers
from .affiliate_users_history import AffiliateUsersHistory
from .affiliate_users_withdraw import AffiliateUsersWithdraw

# 2 tables (done)
from .positions import Positions
from .position_users import PositionUsers

# 10 tables (done)
from .follow import Follow
from .personal_wallet_assets import PersonalWalletAssets
from .stocks_balance import StocksBalance
from .tags import Tags
from .user_api import UserAPI
from .user_orders import UserOrders
from .wallet import Wallet
from .wallet_balances import WalletBalances
from .wallet_info import WalletInfo
from .wallet_tags import WalletTags

# 6 tables (done)
from .accounts import Accounts
from .blum_account_statistics import BlumAccountStatistics
from .hamster_account_statistics import HamsterAccountStatistics
from .hamster_upgrade_purchases import HamsterUpgradePurchases
from .tapswap_account_statistics import TapswapAccountStatistics
from .horizon_account_statistics import HorizonAccountStatistics

# 22 tables (WinWin) (done)
from .banned_users import BannedUsers
from .cpm_levels import CPMLevels
from .cpm_rewards import CPMRewards
from .leaderboard_ids import LeaderboardIDs
from .leaderboard_positions import LeaderboardPositions
from .leaderboards_data import LeaderboardsData
from .platform_video_ids import PlatformVideoIDs
from .ppc_levels import PPCLevels
from .ppc_rewards import PPCRewards
from .pps_levels import PPSLevels
from .pps_rewards import PPSRewards
from .referral_activities import ReferralActivities
from .requests import Requests
from .transaction_types import TransactionTypes
from .user_purchases import UserPurchases
from .user_referrals import UserReferrals
from .user_transactions import UserTransactions
from .user_videos import UserVideos
from .user_withdrawals import UserWithdrawals
from .winwin_users import WinWinUsers
from .video_types import VideoTypes
from .videos import Videos

# 3 tables (bid and sales) (done)
from .bid_and_sale_symbols import BidAndSaleSymbols
from .bid_and_sale_user_symbols import BidAndSaleUserSymbols
from .bid_and_sale_users import BidAndSaleUsers
