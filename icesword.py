#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = "轻量级信息收集利用工具"
__author__ = "jx"
__mtime__ = "17-1-2"

import os
import click
import subprocess

def read_domains(ctx, option, objfile):
    if not objfile:
        return {}

    ctx.obj = {}
    ctx.obj["domains"] = [line.strip() for line in objfile]


@click.group(invoke_without_command=True, context_settings=dict(help_option_names=['-h', '--help']))
@click.option("-f", "--file", callback=read_domains, type=click.File("r"),
              help="a text file with strings of domain name")
@click.option("-d", "--domain",
              help="single domain name")
@click.pass_context
def cli(ctx, **kwargs):
    '''主命令'''
    #print "cli"

    if kwargs.get("domain"):
        if not isinstance(ctx.obj, dict) or not ctx.obj.has_key("domains"):
            ctx.obj = {}
            ctx.obj["domains"] = []
        ctx.obj["domains"].append(kwargs["domain"])

    if not ctx.invoked_subcommand:
        ctx.invoke(all)


@cli.command('-', short_help='-')
@click.pass_context
def all(ctx):
    '''默认模式 调用所有子命令'''
    if isinstance(ctx.obj, dict) and ctx.obj.has_key("domains") and len(ctx.obj["domains"]) > 0:
        ctx.invoke(subdomain)

import sys
@cli.command()
@click.pass_context
def subdomain(ctx):
    '''子命令：仅搜集子域名'''
    subDomainBrutePath = os.path.join("tools", "subDomainsBrute")
    popen = subprocess.Popen(["python", "subDomainsBrute.py", ctx.obj["domains"][0]], cwd = subDomainBrutePath,stdout = subprocess.PIPE)
    while True:
        line = popen.stdout.readline()
        r = popen.poll()
        if line == "" and r:
            break
        sys.__stdout__.write(line)
        sys.__stdout__.flush()

def main():
    cli()

if __name__ == "__main__":
    main()
