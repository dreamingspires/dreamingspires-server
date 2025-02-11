from flask import render_template_string
from app import app

class JobListing():
    def __init__(self, job_link, title, date, ect, cost, organisation, organisation_link, department, department_link, tags, description, colour, image_link):
        self.kwargs = {}
        self.kwargs['job_link'] = job_link
        self.kwargs['title'] = title
        self.kwargs['date'] = date
        self.kwargs['ect'] = ect
        self.kwargs['cost'] = cost
        self.kwargs['organisation'] = organisation
        self.kwargs['organisation_link'] = organisation_link
        self.kwargs['department'] = department
        self.kwargs['department_link'] = department_link
        self.kwargs['tags'] = tags
        self.kwargs['description'] = description
        self.kwargs['colour'] = colour
        self.kwargs['image_link'] = image_link

    def render(self):
        template = """
            {% if colour is not none %}
            <div class="box" style="background-color: {{ colour }}">
            {% else %}
            <div class="box">
            {% endif %}
                <article class="media">
                    <figure class="media-left">
                        <p class="image is-64x64">
                            {% if image_link is not none %}
                            <img src="{{ image_link }}">
                            {% else %}
                            <img src="https://bulma.io/images/placeholders/128x128.png">
                            {% endif %}
                        </p>
                    </figure>
                    <div class="media-content">
                        <div class="content">
                            <p>
                                <a href="{{ job_link }}">
                                    <strong>{{ title }}</strong>
                                </a>
                                &nbsp
                                <a href="{{ organisation_link }}"><small>{{ organisation }}</small></a>, 
                                <a href="{{ department_link }}"><small>{{ department }}</small></a>
                                <small><i>{{ date }}</i></small>
                                <br>
                                {{ cost }}
                                &nbsp&nbsp&nbsp&nbsp
                                {% if ect %}
                                Est. completion time ≈ {{ ect }}
                                {% endif %}
                                <br>
                                {% for (tag_text, tag_colour, tag_link) in tags %}
                                {% if tag_colour is not none %}
                                <a href="{{ tag_link }}" class="tag has-background-{{ tag_colour }}">
                                {% else %}
                                <a href="{{ tag_link }}" class="tag">
                                {% endif %}
                                    {{ tag_text }}
                                </a>
                                {% endfor %}
                                <br>
                                {{ description }}
                            </p>
                        </div>
                    </div>
                </article>
            </div>
        """

        with app.app_context():
            return render_template_string(template, **self.kwargs)
