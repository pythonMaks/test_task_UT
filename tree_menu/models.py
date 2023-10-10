from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, unique=True) 
    named_url =  models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=255)
    

    def get_full_path(self):       
        base_url = self.named_url or self.url        
        base_url = base_url.strip('/')
        if self.parent:
            return f"{self.parent.get_full_path()}{base_url}/"
        return f"/{base_url}/"
    

    def save(self, *args, **kwargs):       
        self.url = self.get_full_path()
        super(MenuItem, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.name
    
