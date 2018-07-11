# instagram-statistics
[![Build Status](https://travis-ci.org/ahmdrz/instagram-statistics.svg?branch=master)](https://travis-ci.org/ahmdrz/instagram-statistics)

Instagram Statistics using python and jinja2

### How to use

It's so simple.

```bash
  python main.py --username "<username>" --password "<password>"
```

Optional arguments:

`--liker-size` is `Number of likers to see in chart (-1 means all of them)`, default=10

`--feeds` is `Number of feeds to scan (-1 means all of them)`, default=5

`--template` is `Template name, name of file in templates directory`, default='basic'

Screenshot (basic template):

<img align="center" src="https://github.com/ahmdrz/instagram-statistics/blob/master/resources/download.png" alt="instagram statistics github">

### Templates

I'm not a good front-end designer. So I invite others to create templates file and make PR for me. Templates must follow `jinja2` template engine instrucion.

### License
See full license on [this](https://github.com/ahmdrz/instagram-statistics/blob/master/LICENSE) , Under GNU GENERAL PUBLIC LICENSE
