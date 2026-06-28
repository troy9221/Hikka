<a href="https://deepsource.io/gh/troy9221/Hikka/?ref=repository-badge"><img src="https://deepsource.io/gh/troy9221/Hikka.svg/?label=active+issues&show_trend=true&token=IPVI_QX-cSuQSVeVl8cb5PLt" alt="DeepSource"></a>
<a href="https://deepsource.io/gh/troy9221/Hikka/?ref=repository-badge"><img src="https://deepsource.io/gh/troy9221/Hikka.svg/?label=resolved+issues&show_trend=true&token=IPVI_QX-cSuQSVeVl8cb5PLt" alt="DeepSource"></a><br>
<a href="https://www.codacy.com/gh/troy9221/Hikka/dashboard?utm_source=github.com&utm_medium=referral&utm_content=troy9221/Hikka&utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/97e3ea868f9344a5aa6e4d874f83db14"/></a>
<a href="#"><img src="https://img.shields.io/github/languages/code-size/troy9221/Hikka"/></a>
<a href="#"><img src="https://img.shields.io/github/issues-raw/troy9221/Hikka"/></a>
<a href="#"><img src="https://img.shields.io/github/license/troy9221/Hikka"/></a>
<a href="#"><img src="https://img.shields.io/github/commit-activity/m/troy9221/Hikka"/></a><br>
<a href="#"><img src="https://img.shields.io/github/forks/troy9221/Hikka?style=flat"/></a>
<a href="#"><img src="https://img.shields.io/github/stars/troy9221/Hikka"/></a>&nbsp;<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a><br>

<hr>

<b>Внимание: </b>Если вы мнительный человек, вам не следует использовать этот юзербот. Этот юзербот не является вирусом, но может быть использован в злонамеренных целях. Вы несёте ответственность за все действия, совершённые вашим аккаунтом.  
  
**Важное уведомление:** Версии `1.6.4` и `1.7.0` НЕ будут выпущены по причинам, описанным в журнале изменений.  
Разработка начнётся с нуля в рамках нового проекта, о котором будет объявлено позже.  
Начиная с марта 2025 года вы можете подать заявку на ранний этап альфа-тестирования через официальные каналы.  

<hr>
<h2><img src="https://github.com/hikariatama/assets/raw/master/1326-command-window-line-flat.webp" height="54" align="middle"> Установка</h2>

### Страница установки

<img src="https://github.com/hikariatama/assets/raw/master/install_qr.gif" height="256">

<a href="https://t.me/lavhostbot?start=SGlra2E"><img src="https://user-images.githubusercontent.com/36935426/167272288-85f00779-4b98-47da-8d0d-ea2c6370b979.png" height="40"></a>

<h2>Локальная установка:</h2>
Просто выполните эту команду из-под <b>root</b> и следуйте инструкциям установщика:<br>
<code>(wget -qO- https://hikariatama.ru/get_hikka)</code><br>
<br>
<b>Ручная установка (без скрипта):</b><br>
<code>apt update && apt install git libcairo2 -y && git clone https://github.com/troy9221/Hikka && cd Hikka && pip install -r requirements.txt && python3 -m hikka</code><br.>
<i>Если вы на VPS\VDS, добавьте <code>--proxy-pass</code> в конец команды, чтобы открыть SSH-туннель к web-интерфейсу Hikka, или используйте <code>--no-web</code> для завершения настройки в консоли</i><br>
<br>
<b>Дополнительные подробности:</b>

<details>
 <summary>Предустановленный автоматический бэкапер базы данных</summary>
 <img src="https://user-images.githubusercontent.com/36935426/202905566-964d2904-f3ce-4a14-8f05-0e7840e1b306.png" width="300">
</details>
<details>
 <summary>Приветственная информация установки</summary>
 <img src="https://user-images.githubusercontent.com/36935426/202905720-6319993b-697c-4b09-a194-209c110c79fd.png" width="300">
 <img src="https://user-images.githubusercontent.com/36935426/202905746-2a511129-0208-4581-bb27-7539bd7b53c9.png" width="300">
</details>

<hr>
<h2><img src="https://github.com/hikariatama/assets/raw/master/35-edit-flat.webp" height="54" align="middle"> Изменения</h2>

<ul>
 <li>🆕 <b>Последний слой Telegram</b> с реакциями, видео-стикерами и прочим</li>
 <li>🔓 <b>Безопасность</b> улучшена, включая <b>нативное кэширование сущностей</b> и <b>точечные правила безопасности</b></li>
 <li>🎨 <b>UI/UX</b> улучшения</li>
 <li>📼 Улучшенные и новые <b>основные модули</b></li>
 <li>⏱ Быстрые <b>исправления багов</b> (по сравнению с официальными FTG и GeekTG)</li>
 <li>▶️ <b>Инлайн-формы, галереи и списки</b></li>
 <li>🔁 Полная <b>обратная совместимость</b> с модулями FTG, GeekTG и Dragon Userbot</li>
</ul>
<hr>
<h2 border="none"><img src="https://github.com/hikariatama/assets/raw/master/1312-micro-sd-card-flat.webp" height="54" align="middle"> Требования</h2>
<ul>
 <li>Python 3.8+</li>
 <li>API_ID и HASH от <a href="https://my.telegram.org/apps" color="#2594cb">Telegram</a></li>
</ul>
<hr>
<h2 border="none"><img src="https://github.com/hikariatama/assets/raw/master/680-it-developer-flat.webp" height="54" align="middle"> Документация</h2>

Ознакомьтесь с <a href="https://dev.hikka.pw">dev.hikka.pw</a> для документации разработчиков и <a href="https://hikka.pw">hikka.pw</a> для документации пользователей<br>

<hr>
<h2 border="none"><img src="https://github.com/hikariatama/assets/raw/master/981-consultation-flat.webp" height="54" align="middle"> <a href="https://t.me/hikka_talks">Поддержка</a></h2>
<hr>
<h2 border="none"><img src="https://github.com/hikariatama/assets/raw/master/541-hand-washing-step-12-flat.webp" height="54" align="middle"> Возможности</h2>
<table>
 <tr>
  <td>
   <img src="https://github.com/hikariatama/assets/raw/master/1286-three-3-key-flat.webp" height="32" align="middle"><b> Формы — устали писать? Используйте кнопки!</b>
  </td>
  <td>
   <img src="https://github.com/hikariatama/assets/raw/master/61-camera-flat.webp" height="32" align="middle"><b> Галереи — листайте любимые фото прямо в Telegram</b>
  </td>
 </tr>
 <tr>
  <td>
   <img src="https://user-images.githubusercontent.com/36935426/202842205-9a3906f8-37b1-47f4-acd1-ae441f84aeab.gif">
  </td>
  <td>
   <img src="https://user-images.githubusercontent.com/36935426/202842215-b7bddaf2-f544-4823-80b4-5c2cccaf2157.gif">
  </td>
 </tr>
</table>
<table>
 <tr>
  <td>
   <img src="https://github.com/hikariatama/assets/raw/master/216-arrow-5-flat.webp" height="32" align="middle"><b> Инлайн — поделитесь юзерботом с друзьями</b>
  </td>
  <td>
   <img src="https://github.com/hikariatama/assets/raw/master/1054-amazon-echo-speaker-flat.webp" height="32" align="middle"><b> Взаимодействие с ботами — «No PM»? Не проблема. Бот обратной связи к вашим услугам</b>
  </td>
 </tr>
 <tr>
  <td>
   <img src="https://user-images.githubusercontent.com/36935426/202842234-e53f616d-7423-4a64-a5da-fb71282ad2c4.gif">
  </td>
  <td>
   <img src="https://user-images.githubusercontent.com/36935426/160476037-9537f1c7-8b72-408f-b84c-b89825930bf5.gif">
  </td>
 </tr>
</table>
<table>
 <tr>
  <td>
   <img src="https://github.com/hikariatama/assets/raw/master/1140-error-flat.webp" height="32" align="middle"><b> InlineLogs — traceback прямо в сообщении, вызвавшем ошибку</b>
  </td>
  <td>
   <img src="https://github.com/hikariatama/assets/raw/master/35-edit-flat.webp" height="32" align="middle"><b> Grep — выполните команду и получите только нужные строки</b>
  </td>
 </tr>
 <tr>
  <td>
   <img src="https://user-images.githubusercontent.com/36935426/202842250-b60d218e-9df4-47f6-8c67-b2ef641b4d2d.gif">
  </td>
  <td>
   <img src="https://user-images.githubusercontent.com/36935426/202842263-ee2d5c94-3fd5-43b3-b8ac-2397b69e0fc6.gif">
  </td>
 </tr>
</table>

<b>👨‍👦 NoNick, NoNickUser, NoNickCmd, NoNickChat — используйте другой аккаунт для юзербота</b>
<img src="https://user-images.githubusercontent.com/36935426/202842278-37fbc518-1679-45d7-92f5-9e519275630d.png">

<hr>
<i>⚠️ Этот проект предоставляется «как есть». Разработчик не несёт НИКАКОЙ ответственности за любые проблемы, вызванные юзерботом. Устанавливая Hikka, вы берёте все риски на себя. Это, помимо прочего, включает блокировку аккаунта, удалённые (алгоритмами Telegram) сообщения, SCAM-модули, утёкшие сессии (из-за SCAM-модулей). <b>Настоятельно</b> рекомендуется включить защиту от API Flood (.api_fw_protection) и не устанавливать много модулей за раз. Используя Hikka, вы даёте согласие на любые действия, совершаемые вашим аккаунтом в фоновом режиме в целях автоматизации. Пожалуйста, ознакомьтесь с https://core.telegram.org/api/terms для получения дополнительной информации.</i>

<b>Особая благодарность:</b>

<ul>
    <li><a href="https://gitlab.com/hackintosh5">Hackintosh5</a> за FTG, который является основой проекта</li>
    <li><a href="https://t.me/kazunimo">Kazunimo</a> за турецкий языковой пакет</li>
    <li><a href="https://t.me/hegaNET">Hegakura</a> за татарский языковой пакет</li>
    <li><a href="https://t.me/tiefeschwarz">Aldehydesäure</a> за немецкий языковой пакет</li>
    <li><a href="https://t.me/amorescam">Amore</a> за узбекский языковой пакет</li>
    <li><a href="https://t.me/lonami">Lonami</a> за Telethon, который является основой Hikka-TL</li>
    <li><a href="https://github.com/delivrance">Dan</a> за pyrogram, который является основой Hikka-Pyro</li>
</ul>
