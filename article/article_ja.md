LINE Botを作ろう！AWSで実現するサーバーレスコンピューティング
============================================================

はじめに
------------------------------------------------------------

### 記事概要

* [LINEの開発者用SDK](https://github.com/moleike/line-bot-sdk)とAWSを用いてLINE Botを作成します。

### 想定読者

* AWS におけるサーバーレス実現方式や SAM (Serverless Application Model) について学びたい方。
* 何でも良いからとりあえず LINE Bot を作ってみたい方。

### 前提条件

#### AWS

* 利用可能なAWSアカウントを有していること。
* IAMユーザが払い出されており、実施に必要な権限 (ロール, ポリシー 等) が付与されていること。
* AWS CLI がインストールされていること。

#### LINE 

* [LINE Developers](https://developers.line.biz/) の利用登録が完了していること。
* プロバイダの設定が完了していること。※ 作成する Bot (=チャンネル) はプロバイダに紐づきます。

### リソース

本記事で使用するリソースは、GitHubに公開しています。

* [roki18d / line_textractbot | GitHub](https://github.com/roki18d/line_textractbot)

### 動作確認環境

筆者が動作確認を行った環境は以下の通りです。

```sh
# OS
% sw_vers 
ProductName:    macOS
ProductVersion: 12.0.1
BuildVersion:   21A559

# Python
% python --version
Python 3.7.6
```

### 目次

1. 想定成果物について
2. 実施手順
3. 動作確認
4. 落穂拾い


## 1. 想定成果物について

### 結局何ができるの？

### アーキテクチャ



## 2. 実施手順

### 2-1. 事前準備

### 2-2. LINE Channel の作成

### 2-3. 各種 AWS リソース

#### A. Secrets Manager シークレットの作成

#### B. IAM ポリシーの作成

#### C. S3 バケットの作成

### 2-4. Lambda 関数の設定

### 2-5. テンプレートファイルの編集 & パッケージ

### 2-6. アーティファクトのデプロイ

## 3. 動作確認

### 3-1. Lambda 関数のテスト

### 3-2. API Gateway のテスト

### 3-3. Webhook URL のテスト

### 3-4. LINE Bot のテスト


## 4. 落穂拾い

### 4-1. CloudWatch Logs でトラブルシュートする

### 4-2. その他の AI サービスや機械学習モデルを呼び出す


## さいごに


## 参考


---
EOF
