<section class="section">
    <div class="table-container">
        <table class="table">
            {% sort_libraries data.libraries 'last_commit' as libraries %}

            <thead>
                <tr>
                    <td></td>
                    {% for library in libraries %}
                    {% if library.homepage_url %}
                    <th><a href="{{ library.homepage_url }}">{{ library.name }}</a></th>
                    {% elif library.repo_url %}
                    <th><a href="{{ library.repo_url }}">{{ library.name }}</a></th>
                    {% else %}
                    <th>{{ library.name }}</th>
                    {% endif %}
                    {% endfor %}
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <th></th>
                    {% for library in libraries %}
                    <th>{{ library.name }}</th>
                    {% endfor %}
                </tr>
            </tfoot>
            <tbody>
                <tr>
                    <td class="header">Description</td>
                    {% for library in libraries %}
                    {% repo library as metadata %}
                    
                    <td>
                        {{ metadata.description }}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Repo</td>
                    {% for library in libraries %}
                    <td><a href="{{ library.repo_url }}">{{ library.repo_url|cut:'https://'|cut:'github.com/' }}</a></td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">License</td>
                    {% for library in libraries %}
                    {% repo library as metadata %}

                    <td>
                        {{ metadata.license|default:''|safe }}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Size</td>
                    {% for library in libraries %}
                    <td>
                        {{ library.size }}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Last commit</td>
                    {% for library in libraries %}
                    {% repo library as metadata %}

                    <td>
                        {{ metadata.last_commit|humanize_datetime|default:"--" }}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Version</td>
                    {% for library in libraries %}
                    {% repo library as metadata %}

                    <td>
                        {% if metadata.latest_tag %}
                        <a
                            href="{{ library.repo_url }}/releases/tag/{{ metadata.latest_tag }}">{{ metadata.latest_version|default:"--" }}</a>
                        {% else %}
                        {{ metadata.latest_version|default:"--" }}
                        {% endif %}
                    </td>
                    {% endfor %}
                </tr>
                <!--<tr>
                    <td class="header">Commits</td>
                    {% for library in libraries %}
                    <td>
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Authors</td>
                    {% for library in libraries %}
                    <td>
                    </td>
                    {% endfor %}
                </tr>-->
                <tr>
                    <td class="header">Stars</td>
                    {% for library in libraries %}
                    {% repo library as metadata %}

                    <td>
                        {{ metadata.stars|humanize_int|default:"--" }}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Watchers</td>
                    {% for library in libraries %}
                    {% repo library as metadata %}

                    <td>
                        {{ metadata.watchers|humanize_int|default:"--" }}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Forks</td>
                    {% for library in libraries %}
                    {% repo library as metadata %}

                    <td>
                        {{ metadata.forks|humanize_int|default:"--" }}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Open Issues</td>
                    {% for library in libraries %}
                    {% repo library as metadata %}

                    <td>
                        {% if metadata.open_issues %}
                        <a
                            href="{{ library.repo_url }}/issues">{{ metadata.open_issues|humanize_int|default:"--" }}</a>
                        {% else %}
                        {{ metadata.open_issues|humanize_int|default:"--" }}</a>
                        {% endif %}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">CDN</td>
                    {% for library in libraries %}
                    <td>
                        {% if library.cdn_url %}
                        <a href="{{ library.cdn_url }}">{{ library.cdn_url|cut:'https://'|truncatechars:10 }}</a>
                        {% else %}
                        --
                        {% endif %}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td class="header">Web Components</td>
                    {% for library in libraries %}
                    <td style="vertical-align: middle;">
                        {% if library.web_components is True %}
                        <div class="pos">
                            <img src="{% static 'svg/check.svg' %}">
                        </div>
                        {% elif library.web_components is False %}
                        <div class="neg">
                            <img src="{% static 'svg/x.svg' %}">
                        </div>
                        {% endif %}
                    </td>
                    {% endfor %}
                </tr>
                <tr>
                    <td  class="header">IE11 Compatible</td>
                    {% for library in libraries %}
                    <td style="vertical-align: middle;">
                        {% if library.ie11_compatible is True %}
                        <div class="pos">
                            <img src="{% static 'svg/check.svg' %}">
                        </div>
                        {% elif library.ie11_compatible is False %}
                        <div class="neg">
                            <img src="{% static 'svg/x.svg' %}">
                        </div>
                        {% endif %}
                    </td>
                    {% endfor %}
                </tr>
            </tbody>
        </table>
    </div>
</section>