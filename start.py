import ipywidgets as ipw
from IPython.core.display import HTML
from aiidalab.utils import url_for

def get_start_widget(appbase, jupbase, notebase):
    #http://fontawesome.io/icons/
    return ipw.HTML(f"""
    <div align="center">
        <a href="{url_for(appbase + 'qe.ipynb')}" target="_blank">
            <img src="https://gitlab.com/QEF/q-e/raw/develop/logo.jpg" height="120px" width=243px">
        </a>
    </div>
    """)
    
#EOF
