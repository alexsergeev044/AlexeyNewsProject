{% extends "flatpages/default.html" %}

{% block content %}

<form method="post">
{% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Sing up">
</form>

{% endblock %}