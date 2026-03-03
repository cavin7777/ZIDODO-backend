from django.contrib import admin
from .models import User, Location, Quest, UserQuest, Reward, UserReward

admin.site.register(User)
admin.site.register(Location)
admin.site.register(Quest)
admin.site.register(UserQuest)
admin.site.register(Reward)
admin.site.register(UserReward)