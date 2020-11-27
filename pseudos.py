# -*- coding: utf-8 -*-
import ipywidgets as ipw
import tempfile
from threading import Thread
from subprocess import run

import requests
import traitlets



class Spinner(ipw.HTML):
    """Widget that shows a simple spinner if enabled."""

    enabled = traitlets.Bool()

    def __init__(self, spinner_style=None):
        self.spinner_style = f' style="{spinner_style}"' if spinner_style else ''
        super().__init__()

    @traitlets.default('enabled')
    def _default_enabled(self):  # pylint: disable=no-self-use
        return False

    @traitlets.observe('enabled')
    def _observe_enabled(self, change):
        """Show spinner if enabled, otherwise nothing."""
        if change['new']:
            self.value = f"""<i class="fa fa-spinner fa-pulse"{self.spinner_style}></i>"""
        else:
            self.value = ""


class SSSPInstallWidget(ipw.HBox):

    installed = traitlets.Bool().tag(readonly=True)
    busy = traitlets.Bool().tag(readonly=True)

    base_url = 'http://legacy-archive.materialscloud.org/file/2018.0001/v3'

    def __init__(self):

        self.install_button = ipw.Button(
            description='Install pseudos',
            button_style='warning',
            icon='cloud-download',
            tooltip='Download and install the SSSP pseudo potential families.',
            disabled=True,
            )
        self.install_button.on_click(lambda _: self.download())

        self.progress_bar = ipw.FloatProgress(
            min=0,
            max=1.0,
            orientation='horizontal',
            layout={'visibility': 'hidden'},
        )
        self.progress_bar.visibility = False

        self.spinner = Spinner()
        ipw.dlink((self, 'busy'), (self.spinner, 'enabled'))

        super().__init__(children=[self.install_button, self.spinner, self.progress_bar])
        self._refresh_installed()

    def _refresh_installed(self):
        try:
            self.set_trait('busy', True)
            proc = run("verdi data upf listfamilies".split(), capture_output=True, encoding='utf-8')
            self.installed = 'SSSP_1.1_efficiency' in proc.stdout and 'SSSP_1.1_precision' in proc.stdout
        finally:
            self.set_trait('busy', False)

    @traitlets.default('busy')
    def _default_busy(self):
        return False

    @traitlets.observe('busy')
    def _observe_busy(self, change):
        self.install_button.disabled = change['new']

    @traitlets.observe('installed')
    def _observe_installed(self, change):
        self.install_button.layout.visibility = 'hidden' if change['new'] else 'visible'

    def _download_and_install_pseudos(self, *families):
        session = requests.Session()
        self.progress_bar.layout.visibility = 'visible'

        response_accuracy = session.get(f'{self.base_url}/SSSP_accuracy_pseudos.aiida', stream=True)
        response_efficiency = session.get(f'{self.base_url}/SSSP_efficiency_pseudos.aiida', stream=True)

        total_size_in_bytes= int(response_efficiency.headers.get('content-length', 0)) + \
            int(response_accuracy.headers.get('content-length', 0))
        block_size = 50 * 1024 # Kibibyte

        progress = 0
        for response in (response_accuracy, response_efficiency):
            with tempfile.NamedTemporaryFile() as tmpfile:
                for chunk in response.iter_content(block_size):
                    self.progress_bar.value += (len(chunk) / total_size_in_bytes)
                    tmpfile.write(chunk)
                tmpfile.flush()
                run(['verdi', 'import', '-n', tmpfile.name], check=True)

        self.progress_bar.layout.visibility = 'hidden'

    def _download(self):
        try:
            self.set_trait('busy', True)
            self.progress_bar.layout.visibility = 'visible'

            self._download_and_install_pseudos('SSSP_efficiency_pseudos.aiida')
            self._download_and_install_pseudos('SSSP_precision_pseudos.aiida')

            self.progress_bar.layout.visibility = 'hidden'

            self._refresh_installed()
        finally:
            self.set_trait('busy', False)

    def download(self):
        thread = Thread(target=self._download)
        thread.start()
