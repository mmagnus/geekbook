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
}

.index-controls {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 6px;
  margin: 15px 0;
  flex-wrap: wrap;
}

.filter-btn {
  border: 1px solid #4a90e2;
  color: #4a90e2;
  background: transparent;
  padding: 4px 12px;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.filter-btn:hover {
  background: rgba(74, 144, 226, 0.15);
}

.filter-btn.active-filter {
  background: #4a90e2;
  color: #fff;
}

.filter-btn.random-btn {
  border-color: #9ca3af;
  color: #9ca3af;
}

.filter-btn.random-btn:hover {
  background: rgba(156, 163, 175, 0.15);
}

.filter-btn.random-btn.active-filter {
  background: #9ca3af;
  color: #111;
}

.filter-btn.skills-btn {
  border-color: #f59e0b;
  color: #f59e0b;
}

.filter-btn.skills-btn:hover {
  background: rgba(245, 158, 11, 0.15);
}

.filter-btn.skills-btn.active-filter {
  background: #f59e0b;
  color: #111;
}

#table_id {
  width: 100%;
  background-color: #161616;
  color: #f2f2f2;
  border-collapse: separate;
  border-spacing: 0;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.4);
}

#table_id thead th {
  background-color: #232323;
  color: #f5f5f5;
  border-bottom: 2px solid #3a3a3a;
}

#table_id tbody tr {
  background-color: #1b1b1b;
  border-bottom: 1px solid #3a3a3a;
}

#table_id tbody tr:nth-child(even) {
  background-color: #151515;
}

#table_id tbody tr:hover {
  background-color: #272727;
}

#table_id td,
#table_id th {
  color: inherit;
  padding: 12px;
  vertical-align: top;
}

#table_id td span,
#table_id td small {
  color: rgba(245, 245, 245, 0.75);
}

.index_list_a {
  color: #ffffff;
  font-weight: 600;
  text-decoration: none;
}

.index_list_a:hover {
  color: #7aa8ff;
}

.index_date {
  color: #f5f5f5 !important;
}

.dataTables_wrapper .dataTables_filter,
.dataTables_wrapper .dataTables_length,
.dataTables_wrapper .dataTables_info {
  color: rgba(255, 255, 255, 0.7);
}

.dataTables_wrapper .dataTables_filter input,
.dataTables_wrapper .dataTables_length select {
  background-color: rgba(0, 0, 0, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #f5f5f5;
  border-radius: 4px;
  padding: 4px 8px;
}

.dataTables_wrapper .dataTables_length,
.dataTables_wrapper .dataTables_info,
.dataTables_wrapper .dataTables_filter {
  float: none;
  text-align: left;
  margin-top: 12px;
}

.dataTables_wrapper .dataTables_paginate {
  text-align: center;
  padding-top: 15px;
}
</style>

              <div class="index-controls">
                <button id="filter-openfold" class="filter-btn" type="button" data-filter="openfold">OpenFold</button>
                <button class="filter-btn" type="button" data-filter="rnahub">RNAHub</button>
                <button class="filter-btn" type="button" data-filter="trx">TRX</button>
                <button class="filter-btn skills-btn" type="button" data-filter="skills">Skills</button>
                <button id="random-note-btn" class="filter-btn random-btn" type="button">Random</button>
              </div>

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
                    desc = desc.replace('#fixed', '<span class="label label-success">#fixed</span>')
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
                                 + mdfn + '</a>' + '</br><span style="font-size:10px;color:#f5f5f5">' + desc + '</span></td>' \
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

        html += "</tbody></table>"

        f = open(PATH_TO_HTML + 'index.html', 'w')
        f.write(html)
        f.close()
