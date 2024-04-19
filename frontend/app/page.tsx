import Header from "@/app/components/header";
import ChatSection from "./components/chat-section";
import UserPopup from "./components/user-popup";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center gap-10  ">
      <div
        className="abslute w-full h-full bg-black bg-opacity-50 rounded-3xl "
        style={{
          position: "absolute",
          minHeight: "100%",
          minWidth: "100%",
          zIndex: 1,
        }}
      >
        <video
          autoPlay
          loop
          muted
          disableRemotePlayback
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            zIndex: -1,
          }}
        >
          <source src="/DNA.webm" type="video/webm" />
        </video>

        <div className="flex flex-col mt-20 mx-auto">
          <div className="flex flex-col mx-auto mb-5 bg-slate-800 p-4 rounded-3xl">
            <Header />
          </div>
          <div className="flex flex-row mx-auto space-x-4">
            <div className=" rounded-3xl mx-4 min-w-[300px]">
              <UserPopup />
            </div>
            <ChatSection />
          </div>
        </div>
      </div>
    </main>
  );
}
