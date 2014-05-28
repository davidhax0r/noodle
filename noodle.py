import click
import soundcloud
import re
import requests
import termcolor
import webbrowser

client_id = "1aea2254e453493e8ae85733dba02ec5"


class Noodle(object):
    def __init__(self, url, id=None):
        self.url = url

    @staticmethod
    def is_valid_url(url):
        """
        Validates the URL input
        """
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?'
            r'|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if regex.search(url):
            return True
        return False

    def _get_id(self):
        """
        Gets the track id from URL
        """
        client = soundcloud.Client(client_id=client_id)
        track = client.get('/resolve', url=self.url)
        return track.id

    @property
    def _is_downloadable(self):
        """
        Check's whether the track can be downloaded or not due to copyright
        settings by the uploader
        """
        url_one = "http://api.soundcloud.com/tracks/"
        url_two = ".json?client_id=1aea2254e453493e8ae85733dba02ec5"
        endpoint_url = url_one + str(self._get_id()) + url_two
        response = requests.get(endpoint_url).json()
        if response['downloadable'] == 'true':
            return True
        else:
            return False

    @property
    def download_link(self):
        """
        Returns the download link if the track is downloadable
        """
        if self._is_downloadable:
            url_one = "http://api.soundcloud.com/tracks/"
            url_two = ".json?client_id=1aea2254e453493e8ae85733dba02ec5"
            endpoint_url = url_one + str(self._get_id()) + url_two
            response = requests.get(endpoint_url).json()
            return response["download_url"]
        else:
            return False


@click.command()
@click.option('--url', default="", help='URL of the sound.')
@click.version_option()
def downloader(url):
    """
    Takes --url as input and downloads the song from the url
    """
    if not Noodle.is_valid_url(url):
        if url == "":
            msg = termcolor.colored("Enter url with --url paramater :)", 'red')
            click.echo(msg)
        else:
            err_msg = termcolor.colored("Invalid URL format! -__- ", "red")
            click.echo(err_msg)
    else:
        #Strip the URL from any white spaces
        app = Noodle(url.strip())
        if not app.download_link:
            err = termcolor.colored("Sorry, it's copyrighted! :(", "blue")
            click.echo(err)
        else:
            msg = termcolor.color("Here's the link :) : \n", "yellow")
            click.echo(msg)
            click.echo(app.download_link)
            #Opens the download link in users browser
            webbrowser.open(app.download_link)

if __name__ == "__main__":
    downloader()
