#######
Recipes
#######

The following recipes can be used to solve specific use cases.

*******
Records
*******

Use the following function to add references to one or more records from one
App into a field on a record in another App by searching with keywords:

.. code-block:: python

  from swimlane.records import add_references

  refs = add_references(
      # The ID of the record where the refs will be stored
      record_id="5670dcec0e23ab0e4c363e12",
      # The keywords for searching. Any records that match these keywords will
      # be added as references and returned from this function.
      keywords="chisrv7008",
      # The acronym of the App of record_id. You can also specify this app by
      # passing app_id or app_name. 
      app_acronym="SOC",
      # The acronym of the App that will be searched against. You can also 
      # specify this app by passing remote_app_id or remote_app_name. 
      remote_app_acronym="CMDB",
      # The name of the field on record_id that will hold the references. You
      # can also specify this field by passing field_id.
      field_name="References"
  )

  print refs # This is a list of the records that were added as references.
