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

### TODO list

- [ ] Currently it's based on username, We have to change it to user's primary key.

### License
See full license on [this](https://github.com/ahmdrz/instagram-statistics/blob/master/LICENSE) , Under GNU GENERAL PUBLIC LICENSE
