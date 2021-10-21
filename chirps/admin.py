from django.contrib import admin
from .models import Chirp, ChirpLike

# Register your models here.


class ChirpLikeAdmin(admin.TabularInline):
    model = ChirpLike


class ChirpAdmin(admin.ModelAdmin):
    inlines = [ChirpLikeAdmin]
    search_fields = ["user__username", "user__email"]

    class Meta:
        model = Chirp


admin.site.register(Chirp, ChirpAdmin)
