<img src="assets/cover.svg" alt="Yash Agarwal, over a slow star-trail sky, with a constellation of real pull requests." width="100%">

Working professional, contributing to open source.

`C++` `JavaScript` `Python` &nbsp;·&nbsp; 28 public repos &nbsp;·&nbsp; on GitHub since Jan 2022

## Receipts

<img src="assets/receipt.svg" alt="Paper receipt floating in space: 30 pull requests, 23 merged, 6 open, plus 4369 and minus 693 lines." width="100%">

<sub>This page rebuilds itself from the GitHub API every day. [Make your own with orbit-profile](https://github.com/ityashag/orbit-profile).</sub>

30 pull requests to 6 projects (Bug fixes 19 · Other 5 · Docs 3 · Tests 1 · Cleanup 1 · Features 1). 17 of 17 code fixes shipped with tests.

### Where the work went

| Area | Pull requests | Languages | Latest change |
|---|---|---|---|
| AMD Gaia · **Agent UI** | 4 (4 merged) | TypeScript, CSS, JSON | [#7153](https://github.com/amd/gaia/pull/7153) Renaming a chat, toggling private mode, dropping files on a chat, removing a document from a chat, and removing, cancelling or opening a folder in the Document Library now say so when they fail. |
| AMD Gaia · **Agent UI backend** | 3 (3 merged) | Python | [#6972](https://github.com/amd/gaia/pull/6972) When the default chat model is a cloud model GAIA learns about at runtime, such as `opencode.*`, Settings no longer treats it as a local model. |
| AMD Gaia · **Docs** | 3 (3 merged) | Markdown | [#6864](https://github.com/amd/gaia/pull/6864) Corrects the memory guide&#x27;s category count from six to nine and adds the three missing categories: `profile`, `system` and `permission`. |
| KanaDojo · **Community themes** | 3 (1 merged) | JSON | [#34022](https://github.com/lingdojo/kana-dojo/pull/34022) `community-themes.json` lists some themes more than once: `bamboo-shadow` three times, and `koi-glow`, `matcha-drift` and `sundown-shrine` twice each. |
| AMD Gaia · **Command line** | 2 (2 merged) | Python, Markdown | [#7132](https://github.com/amd/gaia/pull/7132) `gaia cache status` now lists every cache GAIA keeps under `~/.gaia/cache`, each with its size and file count, largest first. |
| AMD Gaia · **Document Q&amp;A** | 2 (2 merged) | Python, Markdown | [#7154](https://github.com/amd/gaia/pull/7154) A vision model that is installed but crashing no longer turns a scanned PDF into blank pages. |
| gosnmp/gosnmp · **gosnmp/gosnmp** | 2 (0 merged) | Go | [#651](https://github.com/gosnmp/gosnmp/pull/651) Fixes #646 (item 4 of #601). |
| AMD Gaia · **Agent tools** | 1 (1 merged) | Python, Markdown | [#7131](https://github.com/amd/gaia/pull/7131) A document indexed twice under different names no longer fills the model&#x27;s context with copies of itself. |
| AMD Gaia · **Agents and installs** | 1 (1 merged) | Python | [#6928](https://github.com/amd/gaia/pull/6928) `gaia agent status` now shows the installed version of an agent installed with `pip`. |
| AMD Gaia · **Code search** | 1 (1 merged) | Python, Markdown | [#6975](https://github.com/amd/gaia/pull/6975) With Lemonade down or the embedding model name wrong, code indexing now fails on its first call and says what to do. |
| AMD Gaia · **Model client** | 1 (1 merged) | Python | [#6907](https://github.com/amd/gaia/pull/6907) A cloud model that one part of GAIA has discovered is now recognized as cloud everywhere, from any provider, instead of being treated as if it ran on your PC. |
| AMD Gaia · **Terminal app** | 1 (1 merged) | Go | [#6971](https://github.com/amd/gaia/pull/6971) When an installed agent&#x27;s install record is corrupt, the TUI now says so instead of dropping the agent without a word. |
| AMD Gaia · **Website** | 1 (1 merged) | CSS | [#6859](https://github.com/amd/gaia/pull/6859) Removes styling code the GAIA website no longer used, so the site ships less dead CSS. |
| AMD Gaia · **src** | 1 (1 merged) | Python | [#7163](https://github.com/amd/gaia/pull/7163) When Launchpad&#x27;s API stops answering, the Linux CLI check now says so. |
| Jenkins · **core** | 1 (1 merged) |  | [#27735](https://github.com/jenkinsci/jenkins/pull/27735) In 55 translation files across 21 languages, a message shows `{0}` instead of its value, loses its apostrophe, or reads an argument the code never passes. |
| Jenkins · **src** | 1 (0 merged) |  | [#27739](https://github.com/jenkinsci/jenkins/pull/27739)  |
| MinIO JS · **AWS credentials** | 1 (0 merged) | JavaScript, TypeScript | [#1516](https://github.com/minio/minio-js/pull/1516) Lets the MinIO JavaScript client sign in with AWS credentials on EC2 and in containers, which failed because it read the wrong field name. |
| apache/airflow · **airflow-core** | 1 (0 merged) | Python | [#77011](https://github.com/apache/airflow/pull/77011) A secrets backend&#x27;s kwargs can also be set one key at a time (`AIRFLOWSECRETSBACKEND_KWARG&lt;KEY&gt;`, and the `[workers]` equivalent). |

### Recently merged

- **AMD Gaia** · [name a Launchpad API timeout as an outage](https://github.com/amd/gaia/pull/7163) · <sub>merged</sub><br>
  When Launchpad&#x27;s API stops answering, the Linux CLI check now says so.
- **Jenkins** · [Show values and apostrophes in translated messages](https://github.com/jenkinsci/jenkins/pull/27735) · <sub>merged</sub><br>
  In 55 translation files across 21 languages, a message shows `{0}` instead of its value, loses its apostrophe, or reads an argument the code never passes.
- **AMD Gaia** · [stop indexing on a broken vision model and name it](https://github.com/amd/gaia/pull/7154) · <sub>merged</sub><br>
  A vision model that is installed but crashing no longer turns a scanned PDF into blank pages.
- **AMD Gaia** · [say when chat and Document Library actions fail](https://github.com/amd/gaia/pull/7153) · <sub>merged</sub><br>
  Renaming a chat, toggling private mode, dropping files on a chat, removing a document from a chat, and removing, cancelling or opening a folder in the Document Library now say so when they fail.
- **AMD Gaia** · [read images left unread while the vision model was down](https://github.com/amd/gaia/pull/7133) · <sub>merged</sub><br>
  A PDF or PowerPoint indexed while the vision model was down no longer keeps its images unsearchable for good.

<details>
<summary>All 30 pull requests, each with what it does</summary>
<br>

**AMD Gaia** · 21

- [name a Launchpad API timeout as an outage](https://github.com/amd/gaia/pull/7163) · <sub>merged</sub><br>
  When Launchpad&#x27;s API stops answering, the Linux CLI check now says so.
- [stop indexing on a broken vision model and name it](https://github.com/amd/gaia/pull/7154) · <sub>merged</sub><br>
  A vision model that is installed but crashing no longer turns a scanned PDF into blank pages.
- [say when chat and Document Library actions fail](https://github.com/amd/gaia/pull/7153) · <sub>merged</sub><br>
  Renaming a chat, toggling private mode, dropping files on a chat, removing a document from a chat, and removing, cancelling or opening a folder in the Document Library now say so when they fail.
- [read images left unread while the vision model was down](https://github.com/amd/gaia/pull/7133) · <sub>merged</sub><br>
  A PDF or PowerPoint indexed while the vision model was down no longer keeps its images unsearchable for good.
- [show every cache folder and its size in gaia cache status](https://github.com/amd/gaia/pull/7132) · <sub>merged</sub><br>
  `gaia cache status` now lists every cache GAIA keeps under `~/.gaia/cache`, each with its size and file count, largest first.
- [count identical chunks once in a search and cite every copy](https://github.com/amd/gaia/pull/7131) · <sub>merged</sub><br>
  A document indexed twice under different names no longer fills the model&#x27;s context with copies of itself.
- [stop the Lemonade Server GAIA uses in gaia kill --lemonade](https://github.com/amd/gaia/pull/6991) · <sub>merged</sub><br>
  `gaia kill --lemonade` now stops the Lemonade Server GAIA actually uses.
- [check every mutating request carries x-gaia-ui](https://github.com/amd/gaia/pull/6976) · <sub>merged</sub><br>
  The Agent UI now has a test that fails if a button&#x27;s request goes out without the `x-gaia-ui` header.
- [one embeddings call per batch, fail on the first error](https://github.com/amd/gaia/pull/6975) · <sub>merged</sub><br>
  With Lemonade down or the embedding model name wrong, code indexing now fails on its first call and says what to do.
- [keep the chat-create error clear of the desktop title bar](https://github.com/amd/gaia/pull/6973) · <sub>merged</sub><br>
  In the desktop app, the &quot;chat was created, but…&quot; error can now be selected and copied, and it no longer sits under the Windows window buttons.
- [use the shared cloud catalog for status, preload and local-only](https://github.com/amd/gaia/pull/6972) · <sub>merged</sub><br>
  When the default chat model is a cloud model GAIA learns about at runtime, such as `opencode.*`, Settings no longer treats it as a local model.
- [show install records the TUI cannot read](https://github.com/amd/gaia/pull/6971) · <sub>merged</sub><br>
  When an installed agent&#x27;s install record is corrupt, the TUI now says so instead of dropping the agent without a word.
- [show a pip-installed agent&#x27;s version in agent status](https://github.com/amd/gaia/pull/6928) · <sub>merged</sub><br>
  `gaia agent status` now shows the installed version of an agent installed with `pip`.
- [classify chat helper models with the shared cloud catalog](https://github.com/amd/gaia/pull/6926) · <sub>merged</sub><br>
  A chat meant to stay on your PC is no longer sent to a cloud model just to give it a title.
- [keep the chat-create error until it is dismissed](https://github.com/amd/gaia/pull/6912) · <sub>merged</sub><br>
  The &quot;chat was created, but...&quot; error now stays visible until you dismiss it, and it no longer covers the chat box.
- [recognize cloud models another client discovered](https://github.com/amd/gaia/pull/6907) · <sub>merged</sub><br>
  A cloud model that one part of GAIA has discovered is now recognized as cloud everywhere, from any provider, instead of being treated as if it ran on your PC.
- [cite chat attachments by their own name](https://github.com/amd/gaia/pull/6896) · <sub>merged</sub><br>
  Answers about a file attached with the + button now cite the file&#x27;s own name instead of GAIA&#x27;s internal upload ID: `According to kestrel-plan.pdf, page 1:` rather than `According to f27f4885-cec8-4161-9dbd-ebc8a3c25005.pdf, page 1:`.
- [list all nine knowledge categories](https://github.com/amd/gaia/pull/6864) · <sub>merged</sub><br>
  Corrects the memory guide&#x27;s category count from six to nine and adds the three missing categories: `profile`, `system` and `permission`.
- [use a fact id that exists in the scenario example](https://github.com/amd/gaia/pull/6863) · <sub>merged</sub><br>
  Fixes the `fact_id` in the custom scenario example, which names a fact that doesn&#x27;t exist in the corpus manifest.
- [delete the unused code panel CSS](https://github.com/amd/gaia/pull/6859) · <sub>merged</sub><br>
  Removes styling code the GAIA website no longer used, so the site ships less dead CSS.
- [remove nvm alias step from the Windows tab](https://github.com/amd/gaia/pull/6852) · <sub>merged</sub><br>
  Removes the `nvm alias default 20.20.0` step from the Windows tab of the setup guide, because NVM for Windows has no `alias` command.

**KanaDojo** · 3

- [remove duplicate entries from community-themes.json](https://github.com/lingdojo/kana-dojo/pull/34022) · <sub>open</sub><br>
  `community-themes.json` lists some themes more than once: `bamboo-shadow` three times, and `koi-glow`, `matcha-drift` and `sundown-shrine` twice each.
- [restore themes removed from community-themes.json](https://github.com/lingdojo/kana-dojo/pull/33693) · <sub>open</sub><br>
  Brings back five community themes that two later merges had accidentally deleted.
- [add new Tsuyu Drizzle theme](https://github.com/lingdojo/kana-dojo/pull/33690) · <sub>merged</sub><br>
  Adds the &quot;Tsuyu Drizzle&quot; color theme to `community/content/community-themes.json`, using the values from the issue.

**gosnmp/gosnmp** · 2

- [keep an established v3 authoritative engine ID](https://github.com/gosnmp/gosnmp/pull/651) · <sub>open</sub><br>
  Fixes #646 (item 4 of #601).
- [take the incoming v3 security level from the received msgFlags](https://github.com/gosnmp/gosnmp/pull/650) · <sub>open</sub><br>
  Fixes #643 (item 1 of #601).

**Jenkins** · 2

- [[JENKINS-69347] Prevent enabling a plugin whose dependency is disabled](https://github.com/jenkinsci/jenkins/pull/27739) · <sub>open</sub>
- [Show values and apostrophes in translated messages](https://github.com/jenkinsci/jenkins/pull/27735) · <sub>merged</sub><br>
  In 55 translation files across 21 languages, a message shows `{0}` instead of its value, loses its apostrophe, or reads an argument the code never passes.

**apache/airflow** · 1

- [Hide team scoped per-key secrets backend kwargs in config output](https://github.com/apache/airflow/pull/77011) · <sub>open</sub><br>
  A secrets backend&#x27;s kwargs can also be set one key at a time (`AIRFLOWSECRETSBACKEND_KWARG&lt;KEY&gt;`, and the `[workers]` equivalent).

**MinIO JS** · 1

- [read AccessKeyId in IamAwsProvider credential responses](https://github.com/minio/minio-js/pull/1516) · <sub>open</sub><br>
  Lets the MinIO JavaScript client sign in with AWS credentials on EC2 and in containers, which failed because it read the wrong field name.

</details>

<details>
<summary>What happened to the merged theme?</summary>
<br>

It merged, then a later merge from another PR accidentally removed it along with other themes. I traced that through the commit history and opened the fix listed above. Star counts belong to the projects.

</details>

<details>
<summary>Earlier team projects (8 PRs)</summary>
<br>

| Repository | Pull request | Status |
|---|---|---|
| vvsvipul/happy-heart-hub | [Hhh 20 jenkinsfile integration](https://github.com/vvsvipul/happy-heart-hub/pull/15) | Merged |
| vvsvipul/happy-heart-hub | [refactor dockerCompose file](https://github.com/vvsvipul/happy-heart-hub/pull/14) | Merged |
| vvsvipul/happy-heart-hub | [HHH-16-reduce-replica-to-1-and-enable-database-persistence-in-kubernetes](https://github.com/vvsvipul/happy-heart-hub/pull/12) | Merged |
| vvsvipul/happy-heart-hub | [Set Up Foundational Project Structure](https://github.com/vvsvipul/happy-heart-hub/pull/2) | Merged |
| vvsvipul/happy-heart-hub | [created repository](https://github.com/vvsvipul/happy-heart-hub/pull/1) | Merged |
| Atharv-V/DevOps-Project | [KEY-18 add jenkins file](https://github.com/Atharv-V/DevOps-Project/pull/2) | Merged |
| Atharv-V/DevOps-Project | [KEY-16 created interface](https://github.com/Atharv-V/DevOps-Project/pull/1) | Merged |
| vvsvipul/Space-Invaders-Gesture-Edition | [bug fix in client.py](https://github.com/vvsvipul/Space-Invaders-Gesture-Edition/pull/1) | Merged |

</details>

## Built

- **[Happy Heart Hub](https://github.com/ityashag/HappyHeartHub)** · heart-risk prediction and generative AI, deployed to scale under load
- **[Secured Socket Programming](https://github.com/ityashag/SOCKET_PROGRAMMING)** · private messaging and file sharing with end-to-end encryption
- **[CrewAI Projects](https://github.com/ityashag/crew.ai)** · 7 hands-on projects, from zero to multi-agent systems
- **[OpenAI Agents SDK Projects](https://github.com/ityashag/Open-AI-SDK)** · 7 practical projects, learning the SDK by building

## On my list

- [x] First merged PR in a popular open-source project: [KanaDojo #33690](https://github.com/lingdojo/kana-dojo/pull/33690)
- [x] Spotted a merge that wiped 5 themes from KanaDojo and [opened the fix](https://github.com/lingdojo/kana-dojo/pull/33693)
- [x] First merge at [AMD Gaia](https://github.com/amd/gaia)
- [ ] First merge at [MinIO](https://github.com/minio/minio-js)
- [x] First merged PR in a project with 10k+ stars

<sub>Numbers from the GitHub API, last updated 14 Nov 2026.</sub>
