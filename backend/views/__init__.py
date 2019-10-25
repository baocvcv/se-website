"""import all views here to make views package"""

from .users_views import UserList
from .users_views import UserDetail
from .auth_views import CustomAuthToken
from .verification_views import EmailVerificationView

from .question_views import QuestionList
from .question_views import QuestionDetail
from .knowledge_node_views import KnowledgeNodeList
from .question_bank_views import QuestionBankList
from .question_bank_views import QuestionBankDetail