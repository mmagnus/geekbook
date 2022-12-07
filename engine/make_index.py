#!/usr/bin/env python

"""geekbook - make index

Get the list of md with sys.stdint.read() and generate html index.html.
The top of the html file is defined here, see the html variable.
The second part is generated in the loop, per md make a link in the index.html.
"""

import os
import time
import re

from engine.conf import PATH_TO_HTML, PATH_TO_TEMPLATE, PATH_HOMEPAGE, PATH_TO_MD, PATH_TO_TEMPLATE_HTML  # noqa
FLASK_BASED = True


class Index(object):
    def __init__(self):
        pass

    def update(self, list_md):
        """Update the index page

        :param list_md: is a list of your md files"""

        if FLASK_BASED:  # flask mode
            head = open(PATH_TO_TEMPLATE_HTML).read()
            head = head.replace('{{ url_index }}', PATH_TO_HTML + '/' + 'index.html')
            head = head.replace('href="img/', 'href="' + '/img/')
            head = head.replace('="lib/', '="' + '/lib/')
            head = head.replace('="css/', '="' + '/css/')
            head = head.replace('="js/', '="' + '/js/')

            # remove demo content
            head = re.sub(r'<!-- start of demo -->.*<!-- end of demo -->',
                          r'', head, flags=re.M | re.DOTALL)

            # insert dataTables  "sorting":true,
            head += """
<style>
body {
  background-color: black;
}</style>

              <!--      "paging": false,
                        -->
              <table id="table_id" class="display compact hover">
                  <thead>
                      <tr>
                          <th>Title</th>
                          <th>Last update</th>
                          <th style="text-align:center">#</th>
                      </tr>
                  </thead>
                  <tbody>
            """
            html = head
        else:
            html = open(PATH_TO_TEMPLATE + '/head.html').read()

            html = html.replace('{{ url_index }}', PATH_TO_HTML + '/' + 'index.html')

            # @todo
            html = html.replace('href="img/', 'href="' + PATH_TO_TEMPLATE + '/img/')
            html = html.replace('src="img/', 'src="' + PATH_TO_TEMPLATE + '/img/')
            html = html.replace('="lib/', '="' + PATH_TO_TEMPLATE + '/lib/')
            html = html.replace('="css/', '="' + PATH_TO_TEMPLATE + '/css/')

            # remove demo content
            html = re.sub(r'<!-- start of demo -->.*<!-- end of demo -->',
                          r'', html, flags=re.M | re.DOTALL)
            ##

        for mdfn in list_md:
            if mdfn == 'imgs':
                pass
            else:
                if mdfn.strip():
                    # Insert the description in the index
                    f = open(PATH_TO_MD + os.sep + mdfn)
                    lines = f.readlines()
                    f.seek(0)
                    if lines:  # if the file is empty
                        if lines[0][0] == '#':
                            desc = lines[0][1].strip() # if '# blelbe' -> 'bleble'
                        else:
                            desc = lines[0]
                    else:
                        desc = ''
                    for l in f:
                        # the tag will overwrite this before
                        if l.strip().startswith('[desc:'):
                            desc = l.replace('[desc:', '').replace(']', '').strip()

                    desc = desc.replace('#todo', '<span class="label label-danger">#todo</span>')
                    desc = desc.replace('#work', '<span class="label label-primary">#work</span>')
                    desc = desc.replace('#done', '<span class="label label-success">#done</span>')
                    desc = desc.replace('#progress', '<span class="label label-warning">#progress</span> ')
                    desc = desc.replace('#waiting', '<span class="label label-info">#waiting</span>')

                    mdfn = re.sub('.md$', '', mdfn)  # replace only .md at the very end
                    path = PATH_TO_HTML + '/' + mdfn
                    # if l.find('::')>=0:
                    #    html += '<li class="table_of_content_h2">
                    # <a style="" href="' + path + '.html">' + l + '</a></li>'
                    # else:
                    if FLASK_BASED:
                        html += '<tr><td style=""><a class="index_list_a" href="/view/' + mdfn + '.html">' \
                                 + mdfn + '</a>' + '</br><span style="font-size:10px;color:gray">' + desc + '</td>' \
                                 + '<td style="white-space: nowrap;"><small><center class="index_date">' \
                                 + time.ctime(os.stat(os.path.join(PATH_TO_MD, mdfn + '.md')).st_mtime) \
                                            + '</center></small></td>' \
                                 + '<td><small><center class="index_date">' + str(len(lines)) + '</center>' \
                                 + '</small></td></tr>'


                    else:
                        html += '<tr><td><a class="index_list_a" href="' + path + '.html">' \
                                + mdfn + '</a></td>' + '<td>' + desc + '</td>' \
                                + '<td><small><center class="index_date">' + \
                                time.ctime(os.stat(os.path.join(PATH_TO_MD, mdfn + '.md')
                                                   ).st_mtime) + '</center></small></td></tr>'

        html += '</p>'

        html += "</tbody></table>"

        f = open(PATH_TO_HTML + 'index.html', 'w')
        f.write(html)
        f.close()
