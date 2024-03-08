from django.db import models


class Staff(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE)
    role = models.ForeignKey("staff.Role", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.role}"
