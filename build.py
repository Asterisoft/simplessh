#!/usr/bin/env python3
"""SimpleSSH 公開サイトを 4 言語分generate する。

**手で 8 ファイルを書かない。** 同じ構成のページが 8 枚あると、
直したつもりの 1 枚だけが直って残りが古いまま、という食い違いが必ず起きる。
文言だけを言語ごとに持ち、骨組みは 1 か所から組む。

    python3 build.py        # ルート（日本語）と en/ zh-Hans/ ko/ を書き出す

出力は上書きする。`style.css` は共通なので触らない。
"""
import html
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
ISSUES = "https://github.com/Asterisoft/simplessh/issues"
ISSUE_NEW = ISSUES + "/new"
UPDATED = "2026-09-17"

# 言語コード → (HTML の lang 属性, サイト上のディレクトリ, 切替バーの表示名)
LANGS = [
    ("ja", "ja", "", "日本語"),
    ("en", "en", "en", "English"),
    ("zh-Hans", "zh-Hans", "zh-Hans", "简体中文"),
    ("ko", "ko", "ko", "한국어"),
]

ICON_TERMINAL = ('<rect x="2.5" y="4" width="19" height="16" rx="2.5"/>'
                 '<path d="M7 10l2.6 2.4L7 14.8"/><path d="M12.6 15h4.6"/>')
ICON_FILES = ('<path d="M3 7.5a2 2 0 012-2h4.2l2 2.4H19a2 2 0 012 2v8.6a2 2 0 01-2 2H5a2 2 0 '
              '01-2-2z"/><path d="M12 11.4v5"/><path d="M9.6 13.8L12 11.4l2.4 2.4"/>')
ICON_GRID = ('<rect x="3" y="4.5" width="7" height="7" rx="1.8"/>'
             '<rect x="14" y="4.5" width="7" height="7" rx="1.8"/>'
             '<rect x="3" y="15" width="7" height="4.5" rx="1.5"/>'
             '<rect x="14" y="15" width="7" height="4.5" rx="1.5"/>')
ICON_KEYS = ('<rect x="2.5" y="6.5" width="19" height="11" rx="2"/>'
             '<path d="M6 10h.01M9.4 10h.01M12.8 10h.01M16.2 10h.01"/><path d="M7.4 14h9.2"/>')

T = {}

T["ja"] = {
    "site_title": "SimpleSSH",
    "support_title": "SimpleSSH — サポート",
    "privacy_title": "SimpleSSH — プライバシーポリシー",
    "support_meta": "普段使いに使えるシンプルな SSH ターミナル SimpleSSH（iPhone・iPad・Mac・Apple Vision Pro）のサポートページです。",
    "privacy_meta": "SimpleSSH のプライバシーポリシーです。当社は利用者から情報を収集しません。",
    "nav_support": "サポート", "nav_privacy": "プライバシーポリシー", "nav_contact": "お問い合わせ",
    "eyebrow_support": "SUPPORT", "eyebrow_privacy": "PRIVACY POLICY",
    "hero_h1": "普段使いに使える、<br>シンプルな SSH ターミナル。",
    "hero_p": "SimpleSSH は、iPhone・iPad・Mac・Apple Vision Pro で使える SSH ターミナルです。"
              "派手な機能よりも、ふだん使っている端末の延長のように使えることを大切にしています。"
              "端末と SFTP のファイル一覧を、同じウィンドウのタブの中で並べて使えます。",
    "eyebrow_features": "FEATURES", "h2_features": "できること",
    "cards": [
        (ICON_TERMINAL, "SSH ターミナル",
         "パスワード認証と公開鍵認証（Ed25519 / RSA）に対応しています。踏み台サーバを経由する"
         "多段接続（ProxyJump）が使え、ホスト鍵は初回の接続時に確認して、以後の変化を検出します。"),
        (ICON_FILES, "SFTP でのファイル操作",
         "アップロード・ダウンロード・移動・削除ができます。Markdown の表、画像、HTML、PDF、SVG は"
         "その場でプレビューでき、よく開く場所はブックマークとして接続先の下に並びます。"),
        (ICON_GRID, "接続先の整理",
         "グループと識別色で接続先を分類できます。色はアイコンとタブの両方に出るので、"
         "本番と検証を取り違えにくくなります。ホスト名での絞り込みにも対応しています。"),
        (ICON_KEYS, "入力の支援",
         "iPhone と iPad では、ソフトキーボードの上に Esc・Ctrl・矢印・F1〜F12 などのキー行が出ます。"
         "接続したときに自動で流すスクリプトを接続先ごとに設定でき、ポート転送（ローカル転送）にも対応しています。"),
    ],
    "eyebrow_req": "REQUIREMENTS", "h2_req": "動作環境",
    "req_head": ("PLATFORM", "VERSION"),
    "req_rows": [("iPhone / iPad", "iOS 17・iPadOS 17 以降"),
                 ("Mac", "macOS 15 以降（Apple シリコン）"),
                 ("Apple Vision Pro", "visionOS 1.0 以降")],
    "req_note": "対応言語は、日本語・英語・簡体中文・한국어 です。",
    "eyebrow_contact": "CONTACT", "h2_contact": "お問い合わせ",
    "contact_lead": "ご質問・不具合の報告・機能のご要望をお待ちしています。",
    "contact_p": ("GitHub の Issues で受け付けています。不具合のご報告では、"
                  "{a}・{b}・{c} を書き添えていただけると、調査が早く進みます。"),
    "contact_fields": ("お使いの機種と OS のバージョン", "アプリのバージョン", "何をしたときに何が起きたか"),
    "cta": "問い合わせる", "cta_sub": "GitHub のアカウントが必要です",
    "eyebrow_faq": "FAQ", "h2_faq": "よくある質問",
    "faq": [
        ("接続先の情報や鍵は、どこに保存されますか",
         "接続先の情報はお客様の iCloud（プライベートデータベース）に、パスワードと秘密鍵は"
         "iCloud キーチェーンに保存されます。開発者がこれらを参照する手段はありません。"
         "詳しくは{privacy}をご覧ください。"),
        ("別の端末で登録した接続先が出てきません",
         "同じ Apple アカウントでサインインしていること、iCloud Drive と iCloud キーチェーンが"
         "有効になっていることをご確認ください。同期が使えない状態のときは、一覧の上部にその旨を表示します。"),
        ("踏み台を経由した接続はできますか",
         "できます。接続先の設定で踏み台となるホストを指定すると、多段の接続（ProxyJump）で繋がります。"
         "踏み台は何段でも重ねられます。"),
        ("Intel の Mac で使えますか",
         "現在の Mac 版は Apple シリコン専用です。Intel の Mac には対応していません。"),
    ],
    "privacy_h1": "当社は、利用者から情報を収集しません。",
    "privacy_p": "SimpleSSH には解析ツール・広告・トラッキングが一切入っておらず、"
                 "当社が運用するサーバも存在しません。以下は、そのことを項目ごとに説明したものです。",
    "updated_label": "最終更新日",
    "clauses": [
        ("当社が収集する情報",
         ["当社は、本アプリの利用者から一切の情報を収集しません。本アプリは解析ツール・広告・"
          "トラッキング（利用者を横断して識別する仕組み）を一切組み込んでおらず、"
          "当社が運用するサーバも存在しません。"]),
        ("利用者のデータがどこに保存されるか",
         ["本アプリが扱うデータの保存先は次のとおりです。いずれも利用者ご自身の管理下にあります。",
          "TABLE",
          "iCloud に保存されたデータは利用者の Apple アカウントに属するものであり、"
          "当社はこれを参照する手段を持ちません。Apple による取り扱いについては、"
          "Apple のプライバシーポリシーをご参照ください。"]),
        ("通信先",
         ["本アプリが通信するのは、利用者ご自身が登録した接続先（SSH・SFTP のサーバ）と、"
          "iCloud 同期のための Apple のサーバだけです。当社のサーバへ接続することはありません。"]),
        ("第三者への提供",
         ["当社は利用者の情報を保有しないため、第三者へ提供することもありません。"]),
        ("子どもの個人情報",
         ["本アプリは特定の年齢層を対象とするものではなく、当社は利用者から情報を収集しないため、"
          "子どもの個人情報を取得することもありません。"]),
        ("本ポリシーの変更",
         ["本ポリシーを変更する場合は、本ページを更新し、冒頭の最終更新日を改めます。"]),
        ("お問い合わせ",
         ["本ポリシーおよび本アプリについてのお問い合わせは、GitHub の Issues で受け付けています。",
          "CONTACT"]),
    ],
    "priv_table_head": ("データ", "保存先", "当社からの参照"),
    "priv_table_rows": [
        ("接続先の情報（表示名・ホスト名・ポート・ユーザ名・分類・色など）",
         "端末内のデータベースと、利用者の iCloud（プライベートデータベース）"),
        ("パスワード・秘密鍵", "iCloud キーチェーン（利用者の Apple アカウントで暗号化されます）"),
        ("接続履歴・起動時スクリプト・ブックマーク", "端末内と、利用者の iCloud（プライベートデータベース）"),
        ("端末セッションの記録（既定では無効）", "端末内のみ。iCloud へは同期しません"),
    ],
    "priv_no": "できません",
    "priv_contact_lead": "AsteriSoft LLC",
    "priv_contact_p": "Issues に書き込むには GitHub のアカウントが必要です。",
}

T["en"] = {
    "site_title": "SimpleSSH",
    "support_title": "SimpleSSH — Support",
    "privacy_title": "SimpleSSH — Privacy Policy",
    "support_meta": "Support for SimpleSSH — a simple SSH terminal for everyday use on iPhone, iPad, Mac and Apple Vision Pro.",
    "privacy_meta": "The SimpleSSH privacy policy. We collect no information from the people who use the app.",
    "nav_support": "Support", "nav_privacy": "Privacy", "nav_contact": "Contact",
    "eyebrow_support": "SUPPORT", "eyebrow_privacy": "PRIVACY POLICY",
    "hero_h1": "A simple SSH terminal,<br>for everyday use.",
    "hero_p": "SimpleSSH is an SSH terminal for iPhone, iPad, Mac and Apple Vision Pro. "
              "Rather than showy features, it aims to feel like an extension of the terminal "
              "you already use. The terminal and the SFTP file list sit side by side, "
              "in tabs within one window.",
    "eyebrow_features": "FEATURES", "h2_features": "What you can do",
    "cards": [
        (ICON_TERMINAL, "SSH terminal",
         "Password and public key authentication (Ed25519 / RSA) are supported. You can connect "
         "through a bastion host in several hops (ProxyJump), and host keys are confirmed on the "
         "first connection so later changes are detected."),
        (ICON_FILES, "Files over SFTP",
         "Upload, download, move and delete. Markdown tables, images, HTML, PDF and SVG preview "
         "in place, and places you open often can be kept as bookmarks under their host."),
        (ICON_GRID, "Destinations in order",
         "Group your destinations and give each an identifying color. The color shows on both the "
         "icon and the tab, which makes production and staging hard to mix up. You can also filter "
         "by host name."),
        (ICON_KEYS, "Help with input",
         "On iPhone and iPad a key row above the software keyboard carries Esc, Ctrl, the arrows, "
         "F1–F12 and more. A script can run automatically on connect, set per destination, and "
         "local port forwarding is supported."),
    ],
    "eyebrow_req": "REQUIREMENTS", "h2_req": "Requirements",
    "req_head": ("PLATFORM", "VERSION"),
    "req_rows": [("iPhone / iPad", "iOS 17 / iPadOS 17 or later"),
                 ("Mac", "macOS 15 or later (Apple silicon)"),
                 ("Apple Vision Pro", "visionOS 1.0 or later")],
    "req_note": "Available in Japanese, English, Simplified Chinese and Korean.",
    "eyebrow_contact": "CONTACT", "h2_contact": "Get in touch",
    "contact_lead": "Questions, bug reports and feature requests are all welcome.",
    "contact_p": ("We take them on GitHub Issues. For a bug report, it helps a great deal "
                  "if you include {a}, {b} and {c}."),
    "contact_fields": ("your device and OS version", "the app version",
                       "what you did and what happened"),
    "cta": "Open an issue", "cta_sub": "A GitHub account is required",
    "eyebrow_faq": "FAQ", "h2_faq": "Frequently asked",
    "faq": [
        ("Where are my destinations and keys stored?",
         "Destinations are stored in your own iCloud (a private database), and passwords and "
         "private keys in the iCloud keychain. The developer has no way to read either. "
         "See the {privacy} for details."),
        ("A destination I saved on another device does not appear",
         "Check that both devices are signed in to the same Apple Account and that iCloud Drive "
         "and the iCloud keychain are turned on. When syncing is unavailable, the app says so at "
         "the top of the list."),
        ("Can I connect through a bastion host?",
         "Yes. Name a bastion in the destination's settings and the connection is made in several "
         "hops (ProxyJump). Bastions can be chained as deep as you need."),
        ("Does it run on an Intel Mac?",
         "The current Mac version is for Apple silicon only. Intel Macs are not supported."),
    ],
    "privacy_h1": "We collect no information from you.",
    "privacy_p": "SimpleSSH contains no analytics, no advertising and no tracking, and we run no "
                 "servers of our own. What follows explains that point by point.",
    "updated_label": "Last updated",
    "clauses": [
        ("What we collect",
         ["We collect no information from the people who use this app. It contains no analytics, "
          "no advertising and no tracking (anything that identifies a person across services), "
          "and we run no servers of our own."]),
        ("Where your data is stored",
         ["The app stores data in the places below. All of them are under your own control.",
          "TABLE",
          "Data held in iCloud belongs to your Apple Account, and we have no means of reading it. "
          "For how Apple handles it, please see Apple's privacy policy."]),
        ("What the app talks to",
         ["The app talks only to the destinations you registered yourself (your SSH and SFTP "
          "servers) and to Apple's servers for iCloud sync. It never connects to servers of ours."]),
        ("Sharing with third parties",
         ["Because we hold no information about you, there is nothing for us to share."]),
        ("Children's data",
         ["The app is not directed at any particular age group, and because we collect no "
          "information from anyone, we collect none from children either."]),
        ("Changes to this policy",
         ["If this policy changes, we update this page and revise the date shown at the top."]),
        ("Contact",
         ["Questions about this policy or about the app are taken on GitHub Issues.", "CONTACT"]),
    ],
    "priv_table_head": ("Data", "Where it lives", "Can we read it?"),
    "priv_table_rows": [
        ("Destinations (display name, host, port, user, group, color and so on)",
         "On the device, and in your iCloud (a private database)"),
        ("Passwords and private keys", "The iCloud keychain, encrypted with your Apple Account"),
        ("Connection history, startup scripts, bookmarks",
         "On the device, and in your iCloud (a private database)"),
        ("Terminal session logs (off by default)", "On the device only; never synced to iCloud"),
    ],
    "priv_no": "No",
    "priv_contact_lead": "AsteriSoft LLC",
    "priv_contact_p": "A GitHub account is required to post an issue.",
}

T["zh-Hans"] = {
    "site_title": "SimpleSSH",
    "support_title": "SimpleSSH — 支持",
    "privacy_title": "SimpleSSH — 隐私政策",
    "support_meta": "SimpleSSH 的支持页面。可在 iPhone、iPad、Mac 和 Apple Vision Pro 上日常使用的简洁 SSH 终端。",
    "privacy_meta": "SimpleSSH 的隐私政策。我们不收集用户的任何信息。",
    "nav_support": "支持", "nav_privacy": "隐私政策", "nav_contact": "联系我们",
    "eyebrow_support": "SUPPORT", "eyebrow_privacy": "PRIVACY POLICY",
    "hero_h1": "可以日常使用的，<br>简洁的 SSH 终端。",
    "hero_p": "SimpleSSH 是可在 iPhone、iPad、Mac 和 Apple Vision Pro 上使用的 SSH 终端。"
              "比起花哨的功能，我们更看重它能像平时使用的终端一样自然。"
              "终端与 SFTP 的文件列表，可以在同一个窗口的标签页中并排使用。",
    "eyebrow_features": "FEATURES", "h2_features": "可以做到的事",
    "cards": [
        (ICON_TERMINAL, "SSH 终端",
         "支持密码认证与公钥认证（Ed25519 / RSA）。可经由跳板机建立多级连接（ProxyJump），"
         "并在首次连接时确认主机密钥，此后检测其变化。"),
        (ICON_FILES, "通过 SFTP 操作文件",
         "支持上传、下载、移动与删除。Markdown 表格、图像、HTML、PDF、SVG 可直接预览，"
         "常用位置可保存为书签，显示在所属连接目标之下。"),
        (ICON_GRID, "整理连接目标",
         "可按分组和识别色对连接目标进行分类。颜色会同时显示在图标和标签页上，"
         "不易混淆生产环境与验证环境，也可按主机名筛选。"),
        (ICON_KEYS, "输入辅助",
         "在 iPhone 和 iPad 上，软键盘上方会显示 Esc、Ctrl、方向键、F1〜F12 等按键行。"
         "可为每个连接目标设置在连接时自动执行的脚本，并支持本地端口转发。"),
    ],
    "eyebrow_req": "REQUIREMENTS", "h2_req": "运行环境",
    "req_head": ("PLATFORM", "VERSION"),
    "req_rows": [("iPhone / iPad", "iOS 17・iPadOS 17 及以上"),
                 ("Mac", "macOS 15 及以上（Apple 芯片）"),
                 ("Apple Vision Pro", "visionOS 1.0 及以上")],
    "req_note": "支持语言：日语、英语、简体中文、韩语。",
    "eyebrow_contact": "CONTACT", "h2_contact": "联系我们",
    "contact_lead": "欢迎提出问题、报告缺陷或提出功能需求。",
    "contact_p": "我们通过 GitHub 的 Issues 受理。报告缺陷时，若能附上 {a}、{b}、{c}，将有助于更快地排查。",
    "contact_fields": ("所用机型与系统版本", "应用版本", "进行了什么操作、出现了什么现象"),
    "cta": "提交问题", "cta_sub": "需要 GitHub 账号",
    "eyebrow_faq": "FAQ", "h2_faq": "常见问题",
    "faq": [
        ("连接目标的信息和密钥保存在哪里？",
         "连接目标的信息保存在您自己的 iCloud（专用数据库）中，密码与私钥保存在 iCloud 钥匙串中。"
         "开发者没有任何途径可以查看这些内容。详情请参阅{privacy}。"),
        ("在其他设备上登记的连接目标没有出现",
         "请确认两台设备登录了同一个 Apple 账户，且已开启 iCloud 云盘与 iCloud 钥匙串。"
         "当同步不可用时，应用会在列表上方给出提示。"),
        ("可以经由跳板机连接吗？",
         "可以。在连接目标的设置中指定作为跳板机的主机，即可建立多级连接（ProxyJump）。"
         "跳板机可以叠加任意层数。"),
        ("能在 Intel 的 Mac 上使用吗？",
         "当前的 Mac 版本仅支持 Apple 芯片，不支持 Intel 的 Mac。"),
    ],
    "privacy_h1": "我们不收集用户的任何信息。",
    "privacy_p": "SimpleSSH 中没有任何分析工具、广告或跟踪机制，我们也不运营任何服务器。"
                 "以下逐项说明这一点。",
    "updated_label": "最后更新日",
    "clauses": [
        ("我们收集的信息",
         ["我们不收集本应用用户的任何信息。本应用未加入任何分析工具、广告或跟踪机制"
          "（跨服务识别用户的手段），我们也不运营任何服务器。"]),
        ("用户数据保存在哪里",
         ["本应用处理的数据保存在以下位置，均处于用户本人的管理之下。",
          "TABLE",
          "保存在 iCloud 中的数据属于用户的 Apple 账户，我们没有查看这些数据的途径。"
          "关于 Apple 的处理方式，请参阅 Apple 的隐私政策。"]),
        ("通信对象",
         ["本应用通信的对象，仅限用户自己登记的连接目标（SSH、SFTP 服务器），"
          "以及用于 iCloud 同步的 Apple 服务器。不会连接到我们的服务器。"]),
        ("向第三方提供",
         ["由于我们不持有用户的信息，也就不存在向第三方提供的情况。"]),
        ("儿童的个人信息",
         ["本应用并非面向特定年龄层，且我们不收集任何用户的信息，因此也不会获取儿童的个人信息。"]),
        ("本政策的变更",
         ["如需变更本政策，我们会更新本页面，并修改开头的最后更新日。"]),
        ("联系我们",
         ["关于本政策及本应用的咨询，请通过 GitHub 的 Issues 提出。", "CONTACT"]),
    ],
    "priv_table_head": ("数据", "保存位置", "我们能否查看"),
    "priv_table_rows": [
        ("连接目标的信息（显示名、主机名、端口、用户名、分组、颜色等）",
         "设备内的数据库，以及用户的 iCloud（专用数据库）"),
        ("密码与私钥", "iCloud 钥匙串（以用户的 Apple 账户加密）"),
        ("连接历史、启动脚本、书签", "设备内，以及用户的 iCloud（专用数据库）"),
        ("终端会话记录（默认关闭）", "仅保存在设备内，不同步至 iCloud"),
    ],
    "priv_no": "不能",
    "priv_contact_lead": "AsteriSoft LLC",
    "priv_contact_p": "提交 Issues 需要 GitHub 账号。",
}

T["ko"] = {
    "site_title": "SimpleSSH",
    "support_title": "SimpleSSH — 지원",
    "privacy_title": "SimpleSSH — 개인정보 처리방침",
    "support_meta": "평소에 쓰기 좋은 단순한 SSH 터미널 SimpleSSH(iPhone・iPad・Mac・Apple Vision Pro)의 지원 페이지입니다.",
    "privacy_meta": "SimpleSSH의 개인정보 처리방침입니다. 당사는 이용자로부터 정보를 수집하지 않습니다.",
    "nav_support": "지원", "nav_privacy": "개인정보", "nav_contact": "문의",
    "eyebrow_support": "SUPPORT", "eyebrow_privacy": "PRIVACY POLICY",
    "hero_h1": "평소에 쓰기 좋은,<br>단순한 SSH 터미널.",
    "hero_p": "SimpleSSH는 iPhone・iPad・Mac・Apple Vision Pro에서 쓰는 SSH 터미널입니다. "
              "화려한 기능보다, 평소 쓰던 터미널의 연장선처럼 쓸 수 있는 것을 중요하게 여깁니다. "
              "터미널과 SFTP 파일 목록을, 한 창의 탭 안에서 나란히 쓸 수 있습니다.",
    "eyebrow_features": "FEATURES", "h2_features": "할 수 있는 일",
    "cards": [
        (ICON_TERMINAL, "SSH 터미널",
         "암호 인증과 공개 키 인증(Ed25519 / RSA)을 지원합니다. 배스천 서버를 거치는 다단 연결"
         "(ProxyJump)을 쓸 수 있고, 호스트 키는 첫 연결 시 확인하여 이후의 변화를 감지합니다."),
        (ICON_FILES, "SFTP 파일 작업",
         "업로드・다운로드・이동・삭제를 할 수 있습니다. Markdown 표, 이미지, HTML, PDF, SVG는 "
         "그 자리에서 미리 볼 수 있고, 자주 여는 위치는 북마크로 해당 연결 대상 아래에 놓입니다."),
        (ICON_GRID, "연결 대상 정리",
         "그룹과 식별 색으로 연결 대상을 분류할 수 있습니다. 색은 아이콘과 탭 양쪽에 나타나므로 "
         "운영과 검증을 혼동하기 어렵고, 호스트 이름으로 좁혀 찾을 수도 있습니다."),
        (ICON_KEYS, "입력 지원",
         "iPhone과 iPad에서는 소프트웨어 키보드 위에 Esc・Ctrl・화살표・F1〜F12 등의 키 행이 나타납니다. "
         "연결했을 때 자동으로 실행할 스크립트를 연결 대상마다 설정할 수 있고, 로컬 포트 전달도 지원합니다."),
    ],
    "eyebrow_req": "REQUIREMENTS", "h2_req": "실행 환경",
    "req_head": ("PLATFORM", "VERSION"),
    "req_rows": [("iPhone / iPad", "iOS 17・iPadOS 17 이상"),
                 ("Mac", "macOS 15 이상 (Apple 실리콘)"),
                 ("Apple Vision Pro", "visionOS 1.0 이상")],
    "req_note": "지원 언어는 일본어・영어・중국어 간체・한국어입니다.",
    "eyebrow_contact": "CONTACT", "h2_contact": "문의",
    "contact_lead": "질문・불편 사항 제보・기능 요청을 기다리고 있습니다.",
    "contact_p": "GitHub의 Issues에서 받고 있습니다. 문제를 알려주실 때 {a}・{b}・{c}를 함께 적어 주시면 "
                 "원인을 찾는 데 큰 도움이 됩니다.",
    "contact_fields": ("사용 중인 기기와 OS 버전", "앱 버전", "무엇을 했을 때 어떤 일이 일어났는지"),
    "cta": "문의하기", "cta_sub": "GitHub 계정이 필요합니다",
    "eyebrow_faq": "FAQ", "h2_faq": "자주 묻는 질문",
    "faq": [
        ("연결 대상 정보와 키는 어디에 저장되나요",
         "연결 대상 정보는 사용자 본인의 iCloud(비공개 데이터베이스)에, 암호와 개인 키는 iCloud "
         "키체인에 저장됩니다. 개발자가 이를 열람할 수단은 없습니다. 자세한 내용은 {privacy}를 봐 주세요."),
        ("다른 기기에서 등록한 연결 대상이 보이지 않습니다",
         "두 기기가 같은 Apple 계정으로 로그인되어 있는지, iCloud Drive와 iCloud 키체인이 켜져 "
         "있는지 확인해 주세요. 동기화를 쓸 수 없는 상태에서는 목록 위쪽에 그 사실을 표시합니다."),
        ("배스천을 거쳐 연결할 수 있나요",
         "가능합니다. 연결 대상 설정에서 배스천이 될 호스트를 지정하면 다단 연결(ProxyJump)로 "
         "이어집니다. 배스천은 몇 단이든 겹칠 수 있습니다."),
        ("Intel Mac에서 쓸 수 있나요",
         "현재 Mac 버전은 Apple 실리콘 전용입니다. Intel Mac은 지원하지 않습니다."),
    ],
    "privacy_h1": "당사는 이용자로부터 정보를 수집하지 않습니다.",
    "privacy_p": "SimpleSSH에는 분석 도구・광고・트래킹이 전혀 들어 있지 않으며, 당사가 운영하는 "
                 "서버도 존재하지 않습니다. 아래는 그 점을 항목별로 설명한 것입니다.",
    "updated_label": "최종 업데이트",
    "clauses": [
        ("당사가 수집하는 정보",
         ["당사는 본 앱 이용자로부터 어떠한 정보도 수집하지 않습니다. 본 앱에는 분석 도구・광고・"
          "트래킹(이용자를 서비스 간에 식별하는 장치)이 전혀 들어 있지 않으며, 당사가 운영하는 "
          "서버도 존재하지 않습니다."]),
        ("이용자의 데이터가 어디에 저장되는가",
         ["본 앱이 다루는 데이터의 저장 위치는 다음과 같습니다. 모두 이용자 본인의 관리 아래에 있습니다.",
          "TABLE",
          "iCloud에 저장된 데이터는 이용자의 Apple 계정에 속하며, 당사는 이를 열람할 수단을 갖고 "
          "있지 않습니다. Apple의 취급에 대해서는 Apple의 개인정보 처리방침을 참조해 주세요."]),
        ("통신 대상",
         ["본 앱이 통신하는 대상은 이용자 본인이 등록한 연결 대상(SSH・SFTP 서버)과 iCloud "
          "동기화를 위한 Apple의 서버뿐입니다. 당사의 서버에 접속하는 일은 없습니다."]),
        ("제3자 제공",
         ["당사는 이용자의 정보를 보유하지 않으므로, 제3자에게 제공할 일도 없습니다."]),
        ("아동의 개인정보",
         ["본 앱은 특정 연령층을 대상으로 하지 않으며, 당사는 이용자로부터 정보를 수집하지 않으므로 "
          "아동의 개인정보를 취득하는 일도 없습니다."]),
        ("본 방침의 변경",
         ["본 방침을 변경할 경우, 본 페이지를 갱신하고 상단의 최종 업데이트 날짜를 고칩니다."]),
        ("문의",
         ["본 방침 및 본 앱에 관한 문의는 GitHub의 Issues에서 받고 있습니다.", "CONTACT"]),
    ],
    "priv_table_head": ("데이터", "저장 위치", "당사의 열람"),
    "priv_table_rows": [
        ("연결 대상 정보(표시 이름・호스트 이름・포트・사용자 이름・분류・색 등)",
         "기기 내 데이터베이스와 이용자의 iCloud(비공개 데이터베이스)"),
        ("암호・개인 키", "iCloud 키체인(이용자의 Apple 계정으로 암호화됩니다)"),
        ("연결 기록・시작 스크립트・북마크", "기기 내와 이용자의 iCloud(비공개 데이터베이스)"),
        ("터미널 세션 기록(기본값은 비활성)", "기기 내에만 저장하며 iCloud로 동기화하지 않습니다"),
    ],
    "priv_no": "불가",
    "priv_contact_lead": "AsteriSoft LLC",
    "priv_contact_p": "Issues에 글을 쓰려면 GitHub 계정이 필요합니다.",
}


def rel(dirname, path):
    """出力先ディレクトリから見た相対パス。ルートは階層が 1 つ浅い。"""
    return ("../" if dirname else "") + path


def langbar(dirname, page):
    out = []
    for code, _attr, d, name in LANGS:
        href = ("../" if dirname else "") + (f"{d}/{page}" if d else page)
        cur = ' aria-current="true"' if d == dirname else ""
        out.append(f'<a href="{href}" lang="{code}" hreflang="{code}"{cur}>{name}</a>')
    return "\n        ".join(out)


def head(t, dirname, title_key, meta_key, page):
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{code}" '
        f'href="https://asterisoft.github.io/simplessh/{(d + "/") if d else ""}{page}">'
        for code, _a, d, _n in LANGS)
    return f"""<!DOCTYPE html>
<html lang="{t['_attr']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t[title_key])}</title>
<meta name="description" content="{html.escape(t[meta_key])}">
{alts}
<link rel="alternate" hreflang="x-default" href="https://asterisoft.github.io/simplessh/{page}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Kaku+Gothic+New:wght@400;500;700&family=JetBrains+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="{rel(dirname, 'style.css')}">
</head>
<body>
"""


def topbar(t, dirname, page):
    here = lambda p: ' aria-current="page"' if p == page else ""
    return f"""    <div class="topbar">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">&gt;_</div>
        <span class="brand-name">{t['site_title']}</span>
      </div>
      <div class="right">
        <nav class="nav">
          <a href="./"{here('index.html')}>{t['nav_support']}</a>
          <a href="./privacy.html"{here('privacy.html')}>{t['nav_privacy']}</a>
          <a href="{ISSUES}">{t['nav_contact']}</a>
        </nav>
        <nav class="langbar" aria-label="Language">
        {langbar(dirname, page)}
        </nav>
      </div>
    </div>
"""


def footer(t):
    return f"""<footer>
  <div class="wrap">
    <span>© 2026 AsteriSoft LLC</span>
    <div class="foot-links">
      <a href="./">{t['nav_support']}</a>
      <a href="./privacy.html">{t['nav_privacy']}</a>
    </div>
  </div>
</footer>

</body>
</html>
"""


def contact_block(t, with_sub=True):
    a, b, c = (f'<span class="field">{html.escape(x)}</span>' for x in t["contact_fields"])
    sub = f'\n        <span class="cta-sub">{t["cta_sub"]}</span>' if with_sub else ""
    return f"""    <div class="contact">
      <div class="body">
        <div class="lead">{t['contact_lead']}</div>
        <p>{t['contact_p'].format(a=a, b=b, c=c)}</p>
      </div>
      <div class="cta-col">
        <a class="cta" href="{ISSUE_NEW}">{t['cta']}</a>{sub}
      </div>
    </div>
"""


def support_page(t, dirname):
    cards = "\n".join(f"""      <div class="card">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0A3550" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icon}</svg>
        <h3>{html.escape(title)}</h3>
        <p>{html.escape(body)}</p>
      </div>""" for icon, title, body in t["cards"])

    rows = "\n".join(f'      <div class="row"><span>{html.escape(a)}</span>'
                     f'<span>{html.escape(b)}</span></div>' for a, b in t["req_rows"])

    privacy_link = f'<a href="./privacy.html">{html.escape(t["nav_privacy"])}</a>'
    faq = "\n".join(f"""      <div class="qa">
        <h3>{html.escape(q)}</h3>
        <p>{a.format(privacy=privacy_link) if '{privacy}' in a else html.escape(a)}</p>
      </div>""" for q, a in t["faq"])

    return (head(t, dirname, "support_title", "support_meta", "index.html")
            + f"""
<header class="masthead">
  <div class="wrap">
{topbar(t, dirname, 'index.html')}
    <div class="hero">
      <div class="eyebrow">{t['eyebrow_support']}</div>
      <h1>{t['hero_h1']}</h1>
      <p>{html.escape(t['hero_p'])}</p>
    </div>
  </div>
</header>

<main class="wrap">

  <section>
    <div class="eyebrow-dark">{t['eyebrow_features']}</div>
    <h2>{html.escape(t['h2_features'])}</h2>
    <div class="cards">
{cards}
    </div>
  </section>

  <section>
    <div class="eyebrow-dark">{t['eyebrow_req']}</div>
    <h2>{html.escape(t['h2_req'])}</h2>
    <div class="table cols-2">
      <div class="row head"><span>{t['req_head'][0]}</span><span>{t['req_head'][1]}</span></div>
{rows}
    </div>
    <p class="note">{html.escape(t['req_note'])}</p>
  </section>

  <section>
    <div class="eyebrow-dark">{t['eyebrow_contact']}</div>
    <h2>{html.escape(t['h2_contact'])}</h2>
{contact_block(t)}  </section>

  <section>
    <div class="eyebrow-dark">{t['eyebrow_faq']}</div>
    <h2>{html.escape(t['h2_faq'])}</h2>
    <div class="faq">
{faq}
    </div>
  </section>

</main>

""" + footer(t))


def privacy_page(t, dirname):
    head_cells = "".join(f"<span>{html.escape(x)}</span>" for x in t["priv_table_head"])
    table_rows = "\n".join(
        f"""        <div class="row">
          <span>{html.escape(a)}</span>
          <span>{html.escape(b)}</span>
          <span class="yes">{html.escape(t['priv_no'])}</span>
        </div>""" for a, b in t["priv_table_rows"])
    table = f"""      <div class="table cols-3">
        <div class="row head">{head_cells}</div>
{table_rows}
      </div>"""

    priv_contact = f"""      <div class="contact">
        <div class="body">
          <div class="lead">{t['priv_contact_lead']}</div>
          <p>{html.escape(t['priv_contact_p'])}</p>
        </div>
        <div class="cta-col">
          <a class="cta" href="{ISSUE_NEW}">{t['cta']}</a>
        </div>
      </div>"""

    clauses = []
    for i, (title, parts) in enumerate(t["clauses"], start=1):
        body = []
        for part in parts:
            if part == "TABLE":
                body.append(table)
            elif part == "CONTACT":
                body.append(priv_contact)
            else:
                body.append(f"      <p>{html.escape(part)}</p>")
        clauses.append(f"""    <section>
      <h2><span class="num">{i:02d}</span>{html.escape(title)}</h2>
{chr(10).join(body)}
    </section>""")

    return (head(t, dirname, "privacy_title", "privacy_meta", "privacy.html")
            + f"""
<header class="masthead">
  <div class="wrap">
{topbar(t, dirname, 'privacy.html')}
    <div class="hero compact">
      <div class="eyebrow">{t['eyebrow_privacy']}</div>
      <h1 class="sm">{html.escape(t['privacy_h1'])}</h1>
      <p>{html.escape(t['privacy_p'])}</p>
      <div class="updated">{html.escape(t['updated_label'])} {UPDATED}</div>
    </div>
  </div>
</header>

<main class="wrap">
  <div class="clauses">

{chr(10).join(clauses)}

  </div>
</main>

""" + footer(t))


def main():
    for code, attr, dirname, _name in LANGS:
        t = dict(T[code]); t["_attr"] = attr
        out = ROOT / dirname if dirname else ROOT
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(support_page(t, dirname), encoding="utf-8")
        (out / "privacy.html").write_text(privacy_page(t, dirname), encoding="utf-8")
        print(f"  {code:8} -> {(dirname + '/') if dirname else './'}index.html, privacy.html")


if __name__ == "__main__":
    main()
