from django.contrib import admin
from .models import Room, Team, Member, Booking

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "room_type", "capacity", "is_active")
    list_filter = ("room_type", "is_active")
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created", "is_active")
    list_filter = ("created", "is_active")
    search_fields = ("name",)
    raw_id_fields = ("created_by",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "team", "gender", "age", "created_by", "is_active")
    list_filter = ("gender", "team", "is_active")
    search_fields = ("name", "email")
    raw_id_fields = (
        "team",
        "created_by",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "team", "date", "slot", "is_active")
    list_filter = ("date", "room", "team", "is_active")
    search_fields = ("room__name", "user__username", "team__name")
    raw_id_fields = ("room", "user", "team")
