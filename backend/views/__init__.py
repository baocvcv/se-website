"""import all views here to make views package"""

from .users_views import UserList
from .users_views import UserDetail
from .auth_views import CustomAuthToken
from .verification_views import EmailVerificationView

from .question_view import QuestionList
