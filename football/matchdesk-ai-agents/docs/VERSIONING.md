# Version policy / 버전 규칙

The project VERSION uses major.minor.patch. Preserve original date/version snapshot directories; point the selection JSON at the current package. Use Git commits for tracked changes, never rewrite earlier snapshots to imply a different execution history. The current version is0.4.0; the legacy definition is0.1.0. A repository-wide tag is not created because this project shares a monorepo with unrelated work.

VERSION은 큰변경.기능변경.수정 번호입니다. 기존날짜/버전 폴더는 보존하고 선택JSON으로현재구성을 지정합니다. Git커밋으로변경내역을 남기며 과거 실행주체를 바꾸어기록하지 않습니다. 이프로젝트와무관한작업이공존하는통합저장소이므로 저장소전체태그는 생성하지 않습니다.

publication_manifest.json contains relative paths, byte counts, SHA-256 content hashes and snapshot labels. It excludes itself to avoid a recursive hash. Original local files remain unchanged. Website bodies, personal paths, credentials, workshop materials and unrelated repositories are not part of the public export. Public paths preserve validator compatibility; the included core-data folder is a clearly labelled demonstration subset.

Text hashes describe the published UTF-8/LF representation; binary files retain their original bytes. 공개 텍스트의 해시는 GitHub에 저장한 UTF-8/LF 줄바꿈 기준입니다.

## 0.3.0 publication scope

Viewer revisions v01–v14 remain immutable comparisons. viewer_selection.json separates functional v12 from soft v13 and pixel v14 previews. The HTML now embeds a larger display dataset; the CSV demo is unchanged. Full provider caches, complete modeling CSV and the local admin source report remain outside this release. Archived reviewer command records may retain generic machine paths describing the original execution environment. docs/publication_manifest-0.2.1.json preserves the previous file listing.

## 0.4.0 adopted design

The user adopted the pixel design. index.html is identical to v15, and viewer_selection.json points to it. v13/v14 stay preserved previews, not the current entry. docs/publication_manifest-0.3.0.json preserves the preceding release. No repository-wide tag is used in this multi-project repository.

## 0.5.0 bilingual interface

Both canonical language entries match the preserved v16 snapshots. The 0.4.0 manifest remains in docs/publication_manifest-0.4.0.json. English changes presentation metadata only, preserving all statistics.
