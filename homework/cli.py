import click
from patient import *

@click.group()
def cli():
    pass

@cli.command()
@click.argument('f_name')
@click.argument('l_name')
@click.option('--birth-date', '-a', type=str)
@click.option('--phone', '-a', type=str)
@click.option('--document-type', '-a', type=str)
@click.option('--document-number', '-a', nargs=2, type=str)
def create(f_name, l_name, birth_date, phone, document_type, document_number):
    click.echo("Новый пользователь вроде cоздан")
    document_number = ''.join(document_number)
    pat = Patient(f_name, l_name, birth_date, phone, document_type, document_number)
    pat.save()
    click.echo("Новый пользователь вроде добавлен")

@cli.command()
@click.argument('count', default=True)
def show(count):
    collection = PatientCollection()
    if count != True:
        for patient in collection.limit(count):
            click.echo(patient)
    else:
        for patient in collection.limit(10):
            click.echo(patient)

@cli.command()
def count():
    collection = PatientCollection()
    amount = None
    for iter, patient in enumerate(collection):
        amount = iter
    if amount is not None:
        amount += 1
    else:
        amount = 0
    print(amount)

if __name__ == '__main__':
    cli()