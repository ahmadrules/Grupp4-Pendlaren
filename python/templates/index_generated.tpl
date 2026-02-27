<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <title>PENDLAREN</title>
    <link rel="stylesheet" href="../static/styles.css">
    <link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet"/>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script type="text/javascript"
            src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    <script type="text/javascript" src="../static/script.js" defer></script>
    <script src="../static/script.js" defer></script>

    <script type="text/javascript">
        function login() {
            window.open('http://accounts.spotify.com/authorize?client_id=e6740bb7feb04f329db3f1cf4ebffefe&redirect_uri=https://127.0.0.1:8000/callback&response_type=code&scope=playlist-modify-public playlist-modify-private');
        }
    </script>
</head>
<body>
<header class="site-header">
    <h1 class="logo-title"><u>PENDLAREN</u></h1>
        <div style="margin-top: 0px;">
            {% if not spotify_logged_in %}
            <button onclick="login()">Logga in</button>
            {% else %}
            <button onclick="window.location.href='/logout'" class="btn-login">Logga ut</button>
            {% endif %}
        </div>
</header>

<main class="site-main">
    <div class="main-layout">
        <section class="form-section">
            <form action="https://127.0.0.1:8000/search" method="POST" class="trip-form">
                <div class="form-group">
                    <label for="from">Från:</label>
                    <select class="js-example-basic-single" id="from" name="fromStop">
                    </select>
                </div>

                <div class="form-group">
                    <label for="to">Till:</label>
                    <select class="js-example-basic-single" id="to" name="toStop">
                    </select>
                </div>
                <div class="form-group">
                    <label for="genre">Genre:</label>
                    <select class="js-example-basic-single" id="genre" name="genre">
                        <option value=""> Välj genre</option>
                        <option value="Pop">Pop</option>
                        <option value="Rock">Rock</option>
                        <option value="Rap">Rap</option>
                    </select>
                </div>
                <input type="hidden" value="application/x-www-form-urlencoded" name="contentType">
                <button type="submit" class="btn-search" id="searchBtn">SÖK</button>
            </form>
        </section>

        <section class="playlist-section">
            <div class="playlist-box">
                <img src="{{playlistImage}}" alt="Din spellista visas här" id="playlistImage">
            </div>

            <a href="{{playlistUrl}}" class="btn-play-now" id="playBtn">
                SPELA NU
            </a>
        </section>

        <aside class="playlist-aside" aria-label="Byten längs rutten">
            <h2 class="aside-title">Reseinformation</h2>
            <div class="trip-info">
                <div class="trip-summary">
                    <p><strong>Från:</strong> {{ trip.fromStop }}</p>
                    <p><strong>Avgång:</strong> {{ trip.fromTime[:5] }}</p>
                    <p><strong>Till:</strong> {{ trip.toStop }}</p>
                    <p><strong>Ankomst:</strong> {{ trip.toTime[:5] }}</p>
                    <p><strong>Restid:</strong> {{ trip.totalTime }}</p>
                </div>

                <h3></br>Byten längs rutten</h3>
                {% if transfers and transfers | length > 0 %}
                <ul>
                    {% for t in transfers %}
                    </br>
                    <li>
                        <strong>{{ t.station }}</strong><br>
                        Ankomst: {{ t.arrival }}</br>
                        {% if not t.is_final_destination %}
                        Avgång: {{ t.departure }}</br>
                        </br>Bytestid: {{ t.wait_minutes }} minuter</br>
                        {% else %}
                        <em>Slutdestination</em>
                        {% endif %}
                    </li>
                    {% endfor %}
                </ul>
                {% else %}
                <p>Inga byten på denna resa.</p>
                {% endif %}

        </aside>
    </div>
</main>
<footer class="site-footer">
    <div class="footer-inner">
                <a href="https://www.trafiklab.se/" class="trafiklab-link">
                    <img src="/static/images/script.png" alt="Trafiklabs logga" style="width:105px;height:50px;">
                </a>

                <a href="https://open.spotify.com/">
                    <img src="/static/images/spotify_logo.png" alt="Spotifys logga" style="width:40px;height:40px;">
                </a>
    </div>
</footer>
</body>
</html>