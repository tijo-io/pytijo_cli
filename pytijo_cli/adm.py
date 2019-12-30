import click
import json
from pytijo_api_client import tijoapi
from pytijo_api_client import command
from .common_options import global_options, tijoapi_url_options


@click.group("tijo-adm")
def tijo_adm():
    """
    tijo administrative commands
    """
    pass


@tijo_adm.command(
    name="login", help="Login to Tijo",
)
@click.argument("user", type=click.STRING)
@click.argument("password", type=click.STRING)
@tijoapi_url_options
@global_options
def login(user, password, tijo_base_api, tijo_insecure, tijo_timeout, **kwargs):
    api = tijoapi.TijoApi(
        tijo_api=tijo_base_api, insecure=tijo_insecure, timeout=tijo_timeout,
    )
    if api.login(email=user, password=password, saveToken=True):
        click.echo("successfully login")
    else:
        click.echo("cannot login")
        raise click.Abort()


@tijo_adm.command(
    name="register", help="Register to Tijo",
)
@click.argument("user", type=click.STRING)
@click.argument("password", type=click.STRING)
@click.argument("first-name", type=click.STRING)
@click.argument("last-name", type=click.STRING)
@tijoapi_url_options
@global_options
def register(
    user,
    password,
    first_name,
    last_name,
    tijo_base_api,
    tijo_insecure,
    tijo_timeout,
    **kwargs
):
    api = tijoapi.TijoApi(
        tijo_api=tijo_base_api, insecure=tijo_insecure, timeout=tijo_timeout,
    )
    if api.register(
        email=user, password=password, firstName=first_name, lastName=last_name,
    ):
        click.echo("successfully registered")
    else:
        click.echo("cannot register")
        raise click.Abort()


@tijo_adm.command(
    name="resend", help="Resend verification email",
)
@click.argument("user", type=click.STRING)
@click.argument("password", type=click.STRING)
@tijoapi_url_options
@global_options
def resend(user, password, tijo_base_api, tijo_insecure, tijo_timeout, **kwargs):
    api = tijoapi.TijoApi(
        tijo_api=tijo_base_api, insecure=tijo_insecure, timeout=tijo_timeout,
    )
    if api.resend(email=user, password=password,):
        click.echo("successfully registered")
    else:
        click.echo("cannot register")
        raise click.Abort()


@tijo_adm.command(
    name="reset", help="Reset password via email",
)
@click.argument("reset", type=click.STRING)
@tijoapi_url_options
@global_options
def reset(user, password, tijo_base_api, tijo_insecure, tijo_timeout, **kwargs):
    api = tijoapi.TijoApi(
        tijo_api=tijo_base_api, insecure=tijo_insecure, timeout=tijo_timeout,
    )
    if api.reset(email=user,):
        click.echo("successfully sent password reset email")
    else:
        click.echo("cannot reset password via email")
        raise click.Abort()


@tijo_adm.command(
    name="push",
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    help="Tijo push command to upload new templates. tijo-adm push <template> <any-command>",
)
@click.argument("tijo-template", type=click.File())
@click.option(
    "--tijo-tags", is_flag=True, default=False, help="Tags separated by whitespaces."
)
@click.option(
    "--tijo-include-default-facts",
    is_flag=True,
    default=False,
    help="Add default facts base on this system.",
)
@click.option(
    "--tijo-fact-system", type=click.STRING, default=None, help="Add given system fact."
)
@click.option(
    "--tijo-fact-kernel", type=click.STRING, default=None, help="Add given kernel fact."
)
@click.option(
    "--tijo-fact-machine", type=click.STRING, default=None, help="Add machine fact."
)
@click.option(
    "--tijo-fact-python-version",
    type=click.STRING,
    default=None,
    help="Add python version fact.",
)
@click.option(
    "--tijo-fact-command-path",
    type=click.STRING,
    default=None,
    help="Add command path fact.",
)
@click.option(
    "--tijo-fact-command-path-filesize",
    type=click.STRING,
    default=None,
    help="System fact",
)
@tijoapi_url_options
@global_options
@click.pass_context
def tijo_push(
    ctx,
    tijo_template,
    tijo_tags,
    tijo_include_default_facts,
    tijo_fact_system,
    tijo_fact_kernel,
    tijo_fact_machine,
    tijo_fact_python_version,
    tijo_fact_command_path,
    tijo_fact_command_path_filesize,
    tijo_base_api,
    tijo_insecure,
    tijo_timeout,
    **kwargs
):
    if len(ctx.args) <= 0:
        print("command must be provided.")
        raise click.Abort()

    template = json.load(tijo_template)
    cmd = command.Command(args=ctx.args, template=template)
    api = tijoapi.TijoApi(
        tijo_api=tijo_base_api, insecure=tijo_insecure, timeout=tijo_timeout,
    )

    facts = {}
    if tijo_fact_system:
        facts["system"] = tijo_fact_system
    if tijo_fact_kernel:
        facts["kernel"] = tijo_fact_kernel
    if tijo_fact_machine:
        facts["machine"] = tijo_fact_machine
    if tijo_fact_python_version:
        facts["python_version"] = tijo_fact_python_version
    if tijo_fact_command_path:
        facts["command_path"] = tijo_fact_command_path
    if tijo_fact_command_path_filesize:
        facts["command_path_filesize"] = tijo_fact_command_path_filesize

    template = cmd.push_template(
        api,
        tags=tijo_tags if tijo_tags else None,
        facts=facts if len(facts) > 0 else None,
        facts_attributes=command.DEFAULT_FACTS if tijo_include_default_facts else None,
    )

    if template is not None and "id" in template:
        click.echo(
            "template with id '{}' has been pushed successfully.".format(template["id"])
        )
    else:
        print("template has not been pushed found")
        raise click.Abort()


def main():
    tijo_adm()


if __name__ == "__main__":
    tijo_adm()
