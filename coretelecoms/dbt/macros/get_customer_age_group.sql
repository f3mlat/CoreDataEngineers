{# 
  Categorize a customer's age into standard age groups.
#}

{% macro get_customer_age_group(age_column) %}
    case 
        when {{ age_column }} is null then 'Unknown'
        when {{ age_column }} < 18 then 'Under 18'
        when {{ age_column }} between 18 and 25 then '18-25'
        when {{ age_column }} between 26 and 35 then '26-35'
        when {{ age_column }} between 36 and 50 then '36-50'
        when {{ age_column }} between 51 and 65 then '51-65'
        when {{ age_column }} > 65 then '65+'
        else 'Unknown'
    end
{% endmacro %}
