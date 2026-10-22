
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class User_Table(models.Model):
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    region = models.CharField(max_length=100, default='Kerala')
    status = models.CharField(max_length=10, default='active')
    name = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)





class Follow(models.Model):
    follower = models.ForeignKey(
        User_Table,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        User_Table,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

class Reel(models.Model):
    MEDIA_TYPE_CHOICES = [('video', 'Video'), ('image', 'Image'), ('audio', 'Audio')]
    RESTRICTION_CHOICES = [('approved', 'Approved'), ('under_review', 'Under Review'), ('restricted', 'Restricted')]

    user = models.ForeignKey(User_Table, on_delete=models.CASCADE, related_name='reels')
    media_file = models.FileField(upload_to='reels/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='video')
    caption = models.TextField(blank=True)
    region = models.CharField(max_length=100, default='Kerala')
    place = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_flagged = models.BooleanField(default=False)
    restriction_status = models.CharField(max_length=15, choices=RESTRICTION_CHOICES, default='under_review')
    processing_status = models.CharField(max_length=15, choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)




class ContentAnalysis(models.Model):
    SENTIMENT_CHOICES = [('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative')]
    SAFETY_CHOICES = [('safe', 'Safe'), ('vulgar', 'Vulgar'), ('inappropriate', 'Inappropriate'), ('harmful', 'Harmful'), ('uncertain', 'Uncertain')]

    reel = models.OneToOneField(Reel, on_delete=models.CASCADE, related_name='analysis')
    extracted_text = models.TextField(blank=True)
    transcript = models.TextField(blank=True)
    detected_topic = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=100, blank=True)
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, default='neutral')
    sentiment_score = models.FloatField(default=0.0, validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)])
    safety_status = models.CharField(max_length=15, choices=SAFETY_CHOICES, default='uncertain')
    safety_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    model_confidence = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    is_educational = models.BooleanField(default=False)
    processing_status = models.CharField(max_length=15, choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    model_version = models.CharField(max_length=100, blank=True)
    error_message = models.TextField(blank=True)
    analyzed_at = models.DateTimeField(auto_now=True)



class SafetyAnalysis(models.Model):
    RISK_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('uncertain', 'Uncertain')]

    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='safety_analyses')
    vulgarity_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    inappropriate_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    harmful_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    visual_safety_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    text_safety_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default='uncertain')
    model_version = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



class ContentFlag(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('dismissed', 'Dismissed')]

    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='flags')
    reason = models.TextField()
    confidence = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_content_flags')
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)




class ContentRestriction(models.Model):
    RESTRICTION_CHOICES = [('warning', 'Warning'), ('limited', 'Limited'), ('restricted', 'Restricted'), ('removed', 'Removed'), ('restored', 'Restored')]

    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='restrictions')
    restriction_type = models.CharField(max_length=15, choices=RESTRICTION_CHOICES)
    reason = models.TextField(blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='content_restrictions')
    created_at = models.DateTimeField(auto_now_add=True)



class UserInteraction(models.Model):
    user = models.ForeignKey(User_Table, on_delete=models.CASCADE, related_name='interactions')
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='interactions')
    is_liked = models.BooleanField(default=False)
    is_saved = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    watch_duration = models.PositiveIntegerField(default=0, help_text='Duration watched in seconds')
    completion_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    interacted_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'reel'], name='unique_user_reel_interaction')
        ]



class WatchHistory(models.Model):
    user = models.ForeignKey(User_Table, on_delete=models.CASCADE, related_name='watch_history')
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='watch_history')
    duration = models.PositiveIntegerField(default=0)
    completion_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    watched_at = models.DateTimeField(auto_now_add=True)




class Comment(models.Model):
    user = models.ForeignKey(User_Table, on_delete=models.CASCADE, related_name='comments')
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    is_flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class ReelPredictionAndImpact(models.Model):
    ENGAGEMENT_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    IMPACT_CHOICES = [('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')]

    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='predictions')
    predicted_reach = models.PositiveIntegerField(default=0)
    expected_engagement = models.CharField(max_length=10, choices=ENGAGEMENT_CHOICES, default='medium')
    predicted_engagement_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    recommended_posting_time = models.DateTimeField(null=True, blank=True)
    social_impact_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    social_impact_level = models.CharField(max_length=10, choices=IMPACT_CHOICES, default='moderate')
    model_version = models.CharField(max_length=100, blank=True)
    calculated_at = models.DateTimeField(auto_now_add=True)



class Trend(models.Model):
    topic_name = models.CharField(max_length=150)
    region = models.CharField(max_length=100, default='Kerala')
    frequency_count = models.PositiveIntegerField(default=1)
    trend_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    period_start = models.DateTimeField(null=True, blank=True)
    period_end = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['topic_name', 'region', 'period_start', 'period_end'], name='unique_trend_period')
        ]




class UserInterest(models.Model):
    user = models.ForeignKey(User_Table, on_delete=models.CASCADE, related_name='interests')
    topic = models.CharField(max_length=150)
    interest_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'topic'], name='unique_user_interest')
        ]




class RecommendationLog(models.Model):
    user = models.ForeignKey(User_Table, on_delete=models.CASCADE, related_name='recommendation_logs')
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='recommendation_logs')
    ranking_score = models.FloatField(default=0.0)
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)




class Complaint(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('rejected', 'Rejected')]

    user = models.ForeignKey(User_Table, on_delete=models.CASCADE, related_name='complaints')
    complaint_text = models.TextField()
    reply_text = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    replied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaint_replies')
    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(null=True, blank=True)




class Feedback(models.Model):
    user = models.ForeignKey(User_Table, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_text = models.TextField()
    rating = models.FloatField(default=1.5)
    created_at = models.DateTimeField(auto_now_add=True)

