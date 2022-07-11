cocojson 형태에서 Voc형식으로 반환하고자 할때 사용하시면 됩니다.

다음과 같이 실행해보세요!

!python coco.py "potted plant"

"potted plant"자리에 원하는 class를 넣으면 됩니다.

+)여러 class를 한꺼번에 다운받고자 하는 경우 

!python coco-extractor.py "person" "sports ball" "zebra"

출처 : https://github.com/KaranJagtiani/YOLO-Coco-Dataset-Custom-Classes-Extractor

위의 원본 코드에서 Voc형식으로 자동저장되게 조금 수정한 파일입니다.
