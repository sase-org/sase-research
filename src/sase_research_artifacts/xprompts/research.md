---
description: Write the current research to a new dated file in the research artifact repo.
input:
  - name: report_target
    type: path
    default: null
    description:
      Optional month-relative markdown report path. When set, write exactly this file
      and fail visibly if it already exists.
---

{% if report_target %}
Write this research to exactly this report file:

$(sase repo path research --ensure)/$(date +%Y%m)/{{ report_target }}

Create parent directories if needed. Create the report without overwrite: if the file
already exists, stop and report the collision visibly instead of replacing it.
{% else %}
Write this research to a new markdown file under the $(sase repo path research --ensure)/$(date +%Y%m)/ directory.
{% endif %}
