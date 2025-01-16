import { Innertube } from "youtubei.js";

// Innertube インスタンスを作成
const innertube = new Innertube();

// 動画IDを指定して情報を取得
async function getVideoInfo(videoId) {
    const video = await innertube.getVideoInfo(videoId);
    console.log(video);
}

// 動画の詳細を取得
getVideoInfo("dQw4w9WgXcQ");
