from .base import Base, BaseModel
# 15 tables
from .activated_user_sections import ActivatedUserSections
from .admin_settings import AdminSettings
from .course_placeholders import CoursePlaceholders
from .premium_users import PremiumUsers
from .profiles import Profiles
from .quiz_results import QuizResults
from .reply_messages import ReplyMessages
from .social_networks_links import SocialNetworksLinks
from .subscription_orders import SubscriptionOrders
from .subscription_services import SubscriptionServices
from .subscriptions import Subscriptions
from .user_services import UserServices
from .user_tokens import UserTokens
from .users import Users
from .users_exchange import UsersExchange
# 5 tables
from .closed_leaderboard_orders import ClosedLeaderboardOrders
from .leaderboard_orders import LeaderboardOrders
from .leaderboard_users import LeaderboardUsers
from .auto_order_users import AutoOrderUsers
from .auto_order_users_orders import AutoOrderUsersOrders
# 4 tables
from .forex_signals import ForexSignals
from .forex_users import ForexUsers
from .users_forex_api import UsersForexAPI
from .forex_users_order_history import ForexUsersOrderHistory
# 2 tables
from .klines_pairs import KlinesPairs
from .klines_users import KlinesUsers
# 17 tables
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
# 4 tables
from .payment_numbers import PaymentNumbers
from .purchases import Purchases
from .uzum_app_payment import UzumAppPayment
from .uzum_payment import UzumPayment
# 4 tables (p2p)
from .auto_delete_message import AutoDeleteMessage
from .p2p_pairs import P2PPairs
from .p2p_pairs_exchange import P2PPairsExchange
from .p2p_users import P2PUsers
# 3 tables
from .pairs import Pairs
from .signals_users import SignalsUsers
from .xauusd_signals import XAUUSDSignals
# 3 tables
from .affiliate_users import AffiliateUsers
from .affiliate_users_history import AffiliateUsersHistory
from .affiliate_users_withdraw import AffiliateUsersWithdraw
# 2 tables
from .positions import Positions
from .position_users import PositionUsers
