---
title: theme 설정
linkTitle: theme 설정
description: ""
date: 2023-11-26T08:58:52.784Z
series:
  - Blog
categories:
  - Blog
tags:
  - Hugo
authors:
  - Hyunyoun Jo
lastmod: 2024-01-02T22:16:32
draft: false
featured: true
---

- 참고 : [Hugo Themes](https://themes.gohugo.io/)에 올라와 있는 Theme중에 마음에 드는 걸로 골라서 설치하면 된다.
- 여기 설정된 Theme는 [HB Theme](https://github.com/hbstack/theme)
  - [starter theme template](https://github.com/hbstack/theme)도 제공함.

## Hugo Theme 설치

- [Prerequisites]({{<ref "hugo를-이용한-github-pages-블로그-만들기#Prerequisites">}})을 전부 설치하였으면, 준비가 된 것이다.

- 필자는 [HB Theme](https://github.com/hbstack/theme)을 Submodule로 themes에 추가한 뒤, 상위 폴더에 복사하여 사용하였다.

## Configuration

- config 폴더는 HB Theme의 설정값들이 들어 있는 폴더이다.
- 아래와 같이 폴더가 나뉘어 있다.

  ```tree config
  config
  ├── _default
  │   ├── hugo.toml
  │   ├── languages.toml
  │   ├── menus.en.toml
  │   ├── menus.zh-hans.toml
  │   └── params.toml
  │   └── params.en.toml
  │   └── params.zh-hans.toml
  ├── development
  │   ├── hugo.toml
  │   └── params.toml
  ├── production
  │   ├── hugo.toml
  │   └── params.toml
  └── staging
      ├── hugo.toml
      └── params.toml
  ```

  - 위의 폴더에 대하여 hbstack에서는 이렇게 설명하고 있다.
    | Environment | Description |
    | ----------- | ----------------------------------------------------------------------------- |
    | \_default | The default configuration, which will be merged into the final configuration. |
    | development | Development environment, the hugo server default environment. |
    | staging | Custom environment, can be loaded by `-e staging`. |
    | production | Production environment, the hugo default environment. |

    필자는 `\_default`, `development`, `production` 3개만 사용하고 있으며, 기본적으로 development, production에서 공통으로 사용되는 값들은 `\_default`에 설정하여 사용하고 있다.

  - configuratio file 종류
    | Configuration file | Description |
    |--------------------|-------------|
    |`hugo.*`| Hugo configuration file|
    |`params.*`| parameter configuration|
    |`menus.*` |menu configuration|
    |`languages.*` |Language configuration|

    제작자가 중국인이다 보니, zh-hans(중국어 간체)와 en(영어) 두개로 나눠 있다.
    처음 서버를 시작해 보면,

    ```md
    127.0.0.1:1313/en
    127.0.0.1:1313/zh-hans
    ```

    구분되어 있는데, `\_default`의 **defaultContentLanguageInSubdir**의 설정을 `true-> false` 변경해줘야 한다.
    **defaultContentLanguageInSubdir**에 대한 주석도 `disable this to remove the default language code from URL, i.e. /en/docs -> /docs.`으로 되어 있다.
    zh-hans(중국어 간체)는 필요없다 보니, content 폴더에서 zh-hans가 들어간 파일은 전부 삭제하는 등 추가 작업이 필요.
