<section class="section">
    <div class="table-container">
        <table class="table">
            {% sort_libraries data.libraries 'last_commit' as libraries %}

            <thead>
                <tr>
                    <th class="header">Library</th>
                    <th class="header" style="min-width: 250px;">Description</th>
                    <th class="header">License</th>
                    <th class="header">Gzipped Size</th>
                    <th class="header last-commit">Last commit</th>
                    <th class="header" style="min-width: 100px;">Version</th>
                    <th class="header">Stars</th>
                    <th class="header">Watchers</th>
                    <th class="header">Forks</th>
                    <th class="header">Open Issues</th>
                    <th class="header">Web Components</th>
                    <th class="header">IE11 Compatible</th>
                </tr>
            </thead>
            <tfoot>
                <tr>
                    <th class="header">Library</th>
                    <th class="header">Description</th>
                    <th class="header">License</th>
                    <th class="header">Gzipped Size</th>
                    <th class="header">Last commit</th>
                    <th class="header">Version</th>
                    <th class="header">Stars</th>
                    <th class="header">Watchers</th>
                    <th class="header">Forks</th>
                    <th class="header">Open Issues</th>
                    <th class="header">Web Components</th>
                    <th class="header">IE11 Compatible</th>
                </tr>
            </tfoot>
            <tbody>
                {% for library in libraries %}
                {% repo library as metadata %}
                    <tr>
                        <td>
                            <!-- Library Name -->
                            <div class="header" style="padding-bottom: 12px;">
                                {% if library.homepage_url %}
                                <a href="{{ library.homepage_url }}">{{ library.name }}</a>
                                {% elif library.repo_url %}
                                <a href="{{ library.repo_url }}">{{ library.name }}</a>
                                {% else %}
                                {{ library.name }}
                                {% endif %}
                            </div>

                            {% if library.repo_url %}
                            <span>
                                <a href="{{ library.repo_url }}">
                                    <img src="{% static 'svg/github.svg' %}" class="">
                                </a>
                            </span>
                            {% endif %}

                            {% if library.cdn_url %}
                            <span>
                                <a href="{{ library.cdn_url }}">
                                    <img src="{% static 'svg/globe.svg' %}" class="">
                                </a>
                            </span>
                            {% endif %}
                        </td>

                        <!-- Description -->
                        <td>
                            {{ metadata.description }}
                        </td>

                        <!-- License -->
                        <td>
                            {{ metadata.license|default:''|safe }}
                        </td>

                        <!-- Minified Size -->
                        <td>
                            {{ library.size }}
                        </td>

                        <!-- Last Commit -->
                        <td>
                            {{ metadata.last_commit|humanize_datetime|default:"--" }}
                        </td>

                        <!-- Version -->
                        <td>
                            {% if metadata.latest_tag %}
                            <a
                                href="{{ library.repo_url }}/releases/tag/{{ metadata.latest_tag }}">{{ metadata.latest_version|truncatechars:14|default:"--" }}</a>
                            {% else %}
                            {{ metadata.latest_version|truncatechars:14|default:"--" }}
                            {% endif %}
                        </td>

                        <!-- Stars -->
                        <td>
                            {{ metadata.stars|humanize_int|default:"--" }}
                        </td>

                        <!-- Watchers -->
                        <td>
                            {{ metadata.watchers|humanize_int|default:"--" }}
                        </td>

                        <!-- Forks -->
                        <td>
                            {{ metadata.forks|humanize_int|default:"--" }}
                        </td>

                        <!-- Open Issues -->
                        <td>
                            {% if metadata.open_issues %}
                            <a
                                href="{{ library.repo_url }}/issues">{{ metadata.open_issues|humanize_int|default:"--" }}</a>
                            {% else %}
                            {{ metadata.open_issues|humanize_int|default:"--" }}</a>
                            {% endif %}
                        </td>

                        <!-- Web Components -->
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

                        <!-- IE11 Compatible -->
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
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</section>