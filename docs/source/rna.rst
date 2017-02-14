RNA-pdb-tools
============================================================

You need to install rna-pdb-tools (http://rna-pdb-tools.readthedocs.io/en/latest/) first.

Draw VARNA-based image of RNA secondary structure
------------------------------------------------------------

Type::

  <pre>[ss:rna]
  UUUCUGUAUAAUGCCGAUAAUAAGGUUCGGCAGUUUCUACCAAACAGCCGUAAACUGUUUGACUACAGUAA
  ((.(((((...((((((.........))))))........(((((((.......)))))))..))))).))
  </pre>

.. warning :: Keep exactly the same syntax as above.::

  <pre>[ss:/name of your seq/]
  /seq/
  /ss/
  </pre>
  # ^ not <pre/> nor <pre>. Keep a new line after this syntax.
  So don't do:
  </pre>
  <pre>

.. warning :: This plugin will change your Markdown file, so make sure that your editor will detect this change and ask you to reload the file!

.. automodule:: engine.plugins.draw_secondary_structure
   :members:

to get a VARNA-drawn image of secondary structure.

.. image :: ../imgs/XQxIC1CrCP.gif
