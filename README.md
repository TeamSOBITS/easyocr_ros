<a name="readme-top"></a>

[JA](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# EasyOCR for ROS


<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#概要">概要</a>
    </li>
    <li>
      <a href="#セットアップ">セットアップ</a>
      <ul>
        <li><a href="#環境条件">環境条件</a></li>
        <li><a href="#インストール方法">インストール方法</a></li>
      </ul>
    </li>
    <li><a href="#実行・操作方法">実行・操作方法</a></li>
    <li>
      <a href="#パラメータ">パラメータ</a>
      <ul>
        <li><a href="#launchパラメータ">launchパラメータ</a></li>
        <li><a href="#yamlパラメータ">yamlパラメータ</a></li>
      </ul>
    </li>
    <li><a href="#マイルストーン">マイルストーン</a></li>
    <li><a href="#参考文献">参考文献</a></li>
  </ol>
</details>


## 概要
本リポジトリは、EasyOCRを使用してリアルタイムで画像からテキストを認識するROS2パッケージです.このパッケージは画像トピックを購読し、EasyOCRを使用して画像を処理し、認識されたテキストとバウンディングボックスを公開します.
<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- セットアップ -->
##  セットアップ

ここで，本レポジトリのセットアップ方法について説明してください．


<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 環境条件

まず，以下の環境を整えてから，次のインストール方法に進んでください．
| System  | Version |
| --- | --- |
| Ubuntu | 22.04 (Jammy Jellyfish) |
| ROS    | Humble Hawksbill |
| Python | 3.10 |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### インストール方法
1. ROS2の`src`フォルダに移動します．
    ```sh
    cd ~/colcon_ws/src/
    ```

2. 本レポジトリをcloneします．
    ```sh
    git clone -b humble-devel https://github.com/TeamSOBITS/easyocr_ros.git
    ```
3. レポジトリの中へ移動します．
    ```sh
    cd easyocr_ros/
    ```
4. 依存パッケージをインストールします．
    ```sh
    bash install.sh
    ```
5. パッケージをコンパイルします．
    ```sh
    cd ~/colcon_ws/
    ```
    ```sh
    colcon build --symlink-install
    ```
    ```sh
    source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- 実行・操作方法 -->
## 実行・操作方法

1. RGBカメラを起動する
2. [easy_ocr.launch.py](launch/easy_ocr.launch.py)の**topic_name**をカメラのTopic名に書き換える
3. [easy_ocr.launch.py](launch/easy_ocr.launch.py)を起動する
   ```sh
   ros2 launch easyocr_ros easy_ocr.launch.py
   ```
<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



## パラメータ
### launchパラメータ

以下は[easy_ocr.launch.py](launch/easy_ocr.launch.py)で設定できるパラメータである.


| パラメータ名              | 説明                                                                 | デフォルト値          |
|---------------------------|----------------------------------------------------------------------|-----------------------|
| `topic_name`              | 画像データを購読するトピック名                                       | `/image_raw`          |
| `gpu`                     | OCR処理にGPUを使用するかどうか                                       | `True`                |
| `classifier_name`         | クラス分類器の名前                                                   | `easy_ocr`            |
| `languages`               | EasyOCRで使用する言語(80以上の言語に対応)                                                | `['en']`              |
| `visualize_duration`      | 可視化の間隔（秒）                                                   | `0.0167`              |
| `enable_visualization`    | OCR結果の可視化を有効にするかどうか(有効にすると処理が重くなる可能性があります)                                  | `True`                |
| `grayscale_mode`          | グレースケールモードで画像を処理するかどうか(性能が向上する可能性があります)                          | `False`               |
| `downscale_ratio`         | 画像を処理するための縮小比率（例：`0.5`は元のサイズの2分の1を意味します） | `1.0`                   |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### yamlパラメータ
以下は[config.yaml](params/config.yaml)で設定できるパラメータである.


| パラメータ | 説明 | 影響 |
|------------|------|------|
| `decoder: greedy` | デコーダの種類.Greedyは最も単純なデコーディング方法で、各ステップで最も確率の高い文字を選択します. | 簡単で高速ですが、最適な結果を得られない場合があります. |
| `beamWidth: 5` | ビームサーチデコーダのビーム幅.大きな値はより多くの候補を保持しますが、計算コストが増加します. | 精度が向上する可能性がありますが、処理時間が長くなります. |
| `batch_size: 1` | 一度に処理する画像のバッチサイズ.大きなバッチサイズは処理速度を向上させますが、メモリ使用量が増加します. | 処理速度が向上しますが、メモリ消費が増加します. |
| `workers: 0` | データローダーが使用するスレッド数.0はシングルスレッドを意味します. | スレッド数を増やすとデータ読み込みが高速化されますが、CPUリソースを多く消費します. |
| `allowlist: ''` | 認識する文字のサブセット.特定のタスク（例：ナンバープレート認識）に便利です. | 特定の文字のみを認識することで精度が向上します. |
| `blocklist: ''` | 無視する文字のサブセット.allowlistが指定されている場合は無視されます. | 特定の文字を無視することで精度が向上します. |
| `detail: 1` | 出力の詳細レベル.1は詳細な出力、0は簡略化された出力を意味します. | 詳細な情報を得ることができますが、出力が増加します. |
| `rotation_info: ''` | 各テキストボックスを最も信頼性の高い結果に回転させるための回転情報.例：[90, 180, 270]. | 回転により認識精度が向上しますが、計算コストが増加します. |
| `paragraph: ''` | 結果を段落にまとめるかどうか.読みやすい段落にするためにTrueに設定します. | 読みやすい出力が得られますが、処理が複雑になります. |
| `min_size: 20` | 最小テキストボックスサイズ（ピクセル単位）.この値より小さいテキストボックスはフィルタリングされます. | 小さなテキストボックスを無視することで精度が向上します. |
| `contrast_ths: 0.1` | この値よりコントラストが低いテキストボックスは調整され、モデルに再入力されます. | コントラストの低いテキストの認識精度が向上します. |
| `adjust_contrast: 0.5` | コントラストの低いテキストボックスを調整するための目標コントラストレベル. | コントラストの低いテキストの認識精度が向上します. |
| `filter_ths: 0.003` | テキストボックスのフィルタリング閾値.この値より信頼度が低いテキストボックスはフィルタリングされます. | 信頼度の低いテキストを無視することで精度が向上します. |
| `text_threshold: 0.7` | テキストの信頼度閾値.この値より信頼度が高いテキストのみが認識されます. | 信頼度の高いテキストのみを認識することで精度が向上します. |
| `low_text: 0.4` | テキストの下限スコア.この値より低いスコアのテキストは無視されます. | 信頼度の低いテキストを無視することで精度が向上します. |
| `link_threshold: 0.4` | リンクの信頼度閾値.この値より信頼度が高いリンクのみが認識されます. | 信頼度の高いリンクのみを認識することで精度が向上します. |
| `canvas_size: 2560` | 最大画像サイズ.このサイズより大きい画像はリサイズされます. | 大きな画像を処理する際のメモリ使用量を制御します. |
| `mag_ratio: 1.0` | 画像の拡大率.1.0は拡大なしを意味します. | 画像の拡大により認識精度が向上する場合があります. |
| `slope_ths: 0.1` | テキストの傾斜閾値.この値より傾斜が大きいテキストは無視されます. | 傾斜の大きいテキストを無視することで精度が向上します. |
| `ycenter_ths: 0.5` | テキストの中心のY座標閾値.この値を超えるテキストは無視されます. | テキストの位置に基づいてフィルタリングすることで精度が向上します. |
| `height_ths: 0.5` | テキストの高さ閾値.この値を超えるテキストは無視されます. | テキストの高さに基づいてフィルタリングすることで精度が向上します. |
| `width_ths: 0.5` | テキストの幅閾値.この値を超えるテキストは無視されます. | テキストの幅に基づいてフィルタリングすることで精度が向上します. |
| `y_ths: 0.5` | テキストのY座標閾値.この値を超えるテキストは無視されます. | テキストの位置に基づいてフィルタリングすることで精度が向上します. |
| `x_ths: 1.0` | テキストのX座標閾値.この値を超えるテキストは無視されます. | テキストの位置に基づいてフィルタリングすることで精度が向上します. |
| `add_margin: 0.1` | テキストボックスに追加するマージン.この値はテキストボックスサイズの割合です. | マージンを追加することで認識精度が向上する場合があります. |
| `output_format: standard` | 出力形式.Standardは標準形式を意味します. | 出力形式を指定することで、結果のフォーマットが変わります. |

詳細は
https://www.jaided.ai/easyocr/documentation/
を参照してください

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- マイルストーン -->
## マイルストーン

- [ ] run_controlの実装
- [ ] しきい値の実装
- [ ] 描画するかのパラメータの追加

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- 参考文献 -->
## 参考文献

* [EasyOCR](https://github.com/JaidedAI/EasyOCR)
* [easyocr_ros](https://github.com/knorth55/easyocr_ros)

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/easyocr_ros/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/easyocr_ros/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/easyocr_ros/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/easyocr_ros/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/easyocr_ros.svg?style=for-the-badge
[license-url]: LICENSE
