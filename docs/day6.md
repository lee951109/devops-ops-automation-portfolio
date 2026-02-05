# Day 6 - 통합 자가 치유(Self-Healing) 엔진 구축

## 1. 개요
단순한 컨테이너 실행 여부 감시를 넘어, 애플리케이션 내부의 장애(좀비 프로세스)까지 감지하고 복구하는 모니터링 시스템 구축

## 2. 모니터링 레이어
1. **Infrastructure Layer (L4)**: `docker inspect`를 통해 컨테이너 프로세스 생존 확인.
2. **Application Layer (L7)**: `requests` 모듈을 통해 `/health` 엔드포인트 응답 (200 OK) 확인.


## 3. 핵심 기능
- **Slack 알림**: 장애 발생 시 즉시 슬랙으로 장애 사유(Infra Down vs Zombie Process)와 복구 결과 전송.
- **보안 관리**: WebHook URL을 코드에서 분리하여 OS 환경 변수로 관리.
- **자동 복구**: 장애 감지 시 `docker restart`를 통한 무중단 운영 지원.

## 4. 장애 재현 테스트 (Zombie Process)
- **현상**: 컨테이너는 `Up` 상태이나 내부 앱 에러로 응답 불능인 상황.
- **재현**: `/make-zombie` API를 호출하여 강제로 500 에러 유발.
- **결과**: 통합 엔진이 'Zombie Process' 사유를 정확히 식별하고 컨테이너 재시작 및 알림 성공.