import click
import sys
import os
from dulwich import porcelain as gitp

__version__ = '0.0'


ANSI = {
	'red': '\033[31m',
	'green': '\033[32m',
	'default': '\033[39m',
}


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version of libterm-git and exit')
@click.option('--change-dir', '-C', default='', help='Change to directory before doing anything')
@click.pass_context
def cli(ctx, version, change_dir):
	#click.echo(ANSI['default'], nl=False)
	ctx.ensure_object(dict)
	ctx.obj['repo'] = '.'
	
	if change_dir != '':
		os.chdir(change_dir)
	
	if version:
		click.echo(f'libterm-git version {__version__} by Dull Bananas (https://dull.pythonanywhere.com)')
		sys.exit()


@cli.command()
@click.pass_context
def status(ctx):
	st = gitp.status(ctx.obj['repo'])
	click.echo(repr(st))
	#TODO: add "On branch [branchname]"
	if True: # <-- will be for --long
		click.echo('Changes to be comitted:')
		click.echo('  (use "git reset HEAD <file>..." to unstage)\n'+ANSI['green'])
		for path in st.staged['add']:
			click.echo(f'\tnew file:   {path.decode("utf-8")}')
		
		click.echo(ANSI['default']+'\nUntracked files:')
		click.echo('  (use "git add <file>..." to include in what will be committed)\n'+ANSI['red'])
		for path in st.untracked:
			click.echo(f'\t{path}')
		click.echo()


if __name__ == '__main__':
	cli()
