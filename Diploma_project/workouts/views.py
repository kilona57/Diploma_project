from services.data_processing import get_user_data
from services.generate_ai import ai_generating_training


def generate_training(request):
    user_data = get_user_data(request=request)
    training = ai_generating_training(user_data)
    pass
