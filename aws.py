# coding: utf-8
import getpass
import os
import sys

import boto
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def aws_keys():
    key = os.environ['AWS_ACCESS_KEY_ID']
    secret = os.environ['AWS_SECRET_ACCESS_KEY']
    return key, secret


def connect_s3():
    access_key, access_secret_key = aws_keys()
    conn = boto.connect_s3(access_key, access_secret_key)
    bucket_name = 'sebsbucket'
    bucket = conn.get_bucket(bucket_name)
    return bucket


def my_paginator(query_set, page, view_limit=10, adjacent=2):
    paginator = Paginator(query_set, view_limit)

    try:
        view = paginator.page(page)
    except PageNotAnInteger:
        view = paginator.page(1)
    except EmptyPage:
        view = paginator.page(paginator.num_pages)

    numpages = view.paginator.num_pages
    chunkstart = view.number - adjacent
    chunkend = view.number + adjacent
    ellipsis_pre = True
    ellipsis_post = True

    if chunkstart <= 2:
        ellipsis_pre = False
        chunkstart = 1
        chunkend = max(chunkend, adjacent * 2)

    if chunkend >= (numpages - 1):
        ellipsis_post = False
        chunkend = numpages
        # chunkstart = min(chunkstart, numpages - (adjacent * 2) + 1)

    if chunkstart <= 2:
        ellipsis_pre = False

    pages = list(range(chunkstart, chunkend + 1))

    if ellipsis_pre:
        pages.insert(0, '...')
        pages.insert(0, 1)

    if ellipsis_post:
        pages.append('...')
        pages.append(view.paginator.num_pages)

    view.pages = pages
    return view
