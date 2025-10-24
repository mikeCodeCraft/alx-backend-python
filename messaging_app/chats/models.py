import uuid

from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
	"""User model for messaging app.

	Fields:
	- id: UUID primary key (indexed automatically)
	- first_name: required
	- last_name: required
	- email: unique, required
	- password_hash: required
	- phone_number: optional
	- role: choices (guest, host, admin)
	- created_at: timestamp (auto set on create)
	"""

	class Role(models.TextChoices):
		GUEST = 'guest', 'Guest'
		HOST = 'host', 'Host'
		ADMIN = 'admin', 'Admin'

	user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	first_name = models.CharField(max_length=150)
	last_name = models.CharField(max_length=150)
	email = models.EmailField(unique=True, db_index=True)
	password_hash = models.CharField(max_length=255)
	phone_number = models.CharField(max_length=30, null=True, blank=True)
	role = models.CharField(max_length=10, choices=Role.choices, default=Role.GUEST)
	created_at = models.DateTimeField(default=timezone.now, editable=False)

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'
		indexes = [models.Index(fields=['email'], name='user_email_idx')]

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"{self.first_name} {self.last_name} <{self.email}>"


class Message(models.Model):
    """Message sent from a user.

    Fields:
    - message_id: UUID primary key
    - sender: FK -> User (stored as sender_id)
    - message_body: text content
    - sent_at: timestamp when created
    """

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages',
        db_column='sender_id',
        db_index=True,
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        indexes = [
            models.Index(fields=['sender'], name='message_sender_idx'),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        # Use sender_id to avoid extra DB hit when printing
        return f"Message {self.message_id} from {self.sender_id}"


class Conversation(models.Model):
	"""Conversation between users.

	Fields:
	- conversation_id: UUID primary key
	- participants: many-to-many relation to `User` (creates participants table)
	- created_at: timestamp when conversation was created
	"""

	conversation_id = models.UUIDField(
		primary_key=True, default=uuid.uuid4, editable=False, db_index=True, db_column='conversation_id'
	)
	participants = models.ManyToManyField(
		User,
		related_name='conversations',
	)
	created_at = models.DateTimeField(default=timezone.now, editable=False)

	class Meta:
		verbose_name = 'conversation'
		verbose_name_plural = 'conversations'
		indexes = [models.Index(fields=['created_at'], name='conversation_created_idx')]

	def __str__(self) -> str:  # pragma: no cover - trivial
		return f"Conversation {self.conversation_id} (participants={self.participants.count()})"


