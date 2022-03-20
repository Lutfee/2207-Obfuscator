.class public final Lcom/example/obfuscate_test/MainActivity$onCreate$$inlined$AppBarConfiguration$default$1;
.super Lkotlin/jvm/internal/Lambda;
.source "AppBarConfiguration.kt"

.implements Lkotlin/jvm/functions/Function0;


.annotation system Ldalvik/annotation/EnclosingMethod;
    value = Lcom/example/obfuscate_test/MainActivity;->onCreate(Landroid/os/Bundle;)V
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x19
    name = null
.end annotation

.annotation system Ldalvik/annotation/Signature;
    value = {
        "Lkotlin/jvm/internal/Lambda;",
        "Lkotlin/jvm/functions/Function0<",
        "Ljava/lang/Boolean;",
        ">;"
    }
.end annotation

.annotation system Ldalvik/annotation/SourceDebugExtension;
    value = "SMAP\nAppBarConfiguration.kt\nKotlin\n*S Kotlin\n*F\n+ 1 AppBarConfiguration.kt\nandroidx/navigation/ui/AppBarConfigurationKt$AppBarConfiguration$1\n*L\n1.end annotation

.annotation runtime Lkotlin/Metadata;
    d1 = {
        "\u0000\n\n\u0000\n\u0002\u0010\u000b\n\u0002\u0008\u0002\u0010\u0000\u001a\u00020\u0001H\n\u00a2\u0006\u0002\u0008\u0002\u00a8\u0006\u0003"
    }
    d2 = {
        "<anonymous>",
        "",
        "invoke",
        "androidx/navigation/ui/AppBarConfigurationKt$AppBarConfiguration$1"
    }
    k = 0x3
    mv = {
        0x1,
        0x6,
        0x0
    }
.end annotation


.field public static final INSTANCE:Lcom/example/obfuscate_test/MainActivity$onCreate$$inlined$AppBarConfiguration$default$1;


.method static constructor <clinit>()V
    .locals 1

    new-instance v0, Lcom/example/obfuscate_test/MainActivity$onCreate$$inlined$AppBarConfiguration$default$1;

    invoke-direct {v0}, Lcom/example/obfuscate_test/MainActivity$onCreate$$inlined$AppBarConfiguration$default$1;-><init>()V

    sput-object v0, Lcom/example/obfuscate_test/MainActivity$onCreate$$inlined$AppBarConfiguration$default$1;->INSTANCE:Lcom/example/obfuscate_test/MainActivity$onCreate$$inlined$AppBarConfiguration$default$1;

    return-void
.end method

.method public constructor <init>()V
    .locals 1

    const/4 v0, 0x0

    invoke-direct {p0, v0}, Lkotlin/jvm/internal/Lambda;-><init>(I)V

    return-void
.end method


.method public bridge synthetic invoke()Ljava/lang/Object;
    .locals 1

    invoke-virtual {p0}, Lcom/example/obfuscate_test/MainActivity$onCreate$$inlined$AppBarConfiguration$default$1;->invoke()Z

    move-result v0

    invoke-static {v0}, Ljava/lang/Boolean;->valueOf(Z)Ljava/lang/Boolean;

    move-result-object v0

    return-object v0
.end method

.method public final invoke()Z
    .locals 1

    const/4 v0, 0x0

    return v0
.end method
