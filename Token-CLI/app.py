import click

@click.command()
@click.option('--name', prompt='what is your name' ,help='provide your name')

def hello(name):
	""" outputs hello """
	click.echo(f'Hello {name}')

if __name__ == '__main__':
	hello()