# MatchDesk 0.9.1 · Portable CSS content hashes

Windows에서 저장소를 내려받으면 CSS 줄바꿈이 LF에서 CRLF로 바뀔 수 있습니다. 0.9.0 검사기는 CSS를 텍스트 정규화 대상에서 빠뜨려 내용이 같아도 파일 명세 검사가 실패했습니다.

이번 수정은 `.css`를 기존 UTF-8/LF 정규화 목록에 추가합니다. 원본 CSS, v23 한영 화면, 11명 재생, 모델, 데이터와 확률은 변경하지 않습니다. 이전 0.9.0 파일 명세를 그대로 보존하고 새 명세는 0.9.1로 기록합니다.

Validation: construct LF and CRLF byte variants in memory from both preserved simulation stylesheets, normalize with the auditor's LF rule, and confirm identical SHA-256 values. Run the publication audit after regenerating the manifest. No browser or paid API call is required for this change.

This patch adds CSS to the existing text normalization rule so the same stylesheet has the same content hash across Git/Windows line endings. The v23 viewers, animation, model and source data remain unchanged. The previous 0.9.0 manifest is preserved byte-for-byte.

[0.9.0 feature SPEC](SPEC-0.9.0.md) · [Preserved 0.9.0 manifest](publication_manifest-0.9.0.json) · [Current manifest](../publication_manifest.json) · [Auditor](../tools/check_release.py)
