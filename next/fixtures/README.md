### What is this directory and files
These directory and files is used for 'fixture', the built-in feature of Django.

### Usage
* Model definition
```
from django.db import models

class Post(models.Model):
    title = models.CharField('Title', max_length=255)

    def __str__(self):
        return self.title
```

* Write contents you wanna insert to DB as json/yaml.
#### json
```
[
  {
    "model": "app.post",
    "pk": 1,
    "fields": {
      "title": "Good morning"
    }
  },
  {
    "model": "app.post",
    "pk": 2,
    "fields": {
      "title": "Hello"
    }
  }
]
```

#### yaml
```
- model: app.post
  pk: 1
  fields:
    Title: Good morning
- model: app.company
  pk: 2
  fields:
    title: Hello
```

* insert the data you've written to DB
```
python manage.py loaddata ${file_name}.{json, yaml}
```


### Attention
In this directory, the extension of the yaml file must be .yaml not .yml
